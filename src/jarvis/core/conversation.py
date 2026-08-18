import asyncio
import logging

from jarvis.audio.io import AudioIO
from jarvis.voice.provider import VoiceProvider

logger = logging.getLogger(__name__)


class Conversation:
    """Orquesta una conversación de voz continua entre el hardware de
    audio (AudioIO) y el proveedor de voz (VoiceProvider).

    No sabe que el audio viene de PyAudio ni que la voz la genera
    Gemini — solo mueve datos entre ambas abstracciones. Barge-in se
    apoya en la detección de actividad nativa del proveedor de voz
    (VAD del lado del servidor): cuando voice.receive() entrega un
    evento "interrupted", esta clase corta la reproducción en curso.

    Recepción y reproducción corren en tareas separadas, conectadas
    por una cola. Esto es a propósito: el proveedor de voz puede
    generar audio más rápido que tiempo real, así que puede haber
    varios chunks ya en camino cuando el usuario interrumpe. Si
    "recibir eventos" y "reproducir audio" fueran la misma tarea
    bloqueante, un evento "interrupted" que llegue detrás de ese
    backlog no se procesaría hasta que todo el backlog terminara de
    sonar — que es exactamente el bug de barge-in tardío que este
    diseño evita.
    """

    def __init__(self, audio: AudioIO, voice: VoiceProvider):
        self.audio = audio
        self.voice = voice
        self._tasks: list[asyncio.Task] = []
        self._playback_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._playback_task: asyncio.Task | None = None

    async def start(self) -> None:
        """Conecta el proveedor de voz, abre el audio, y arranca las
        tareas concurrentes que sostienen la conversación: micrófono
        → voice, voice → cola de reproducción, y cola → parlantes.
        """
        logger.info("Conectando proveedor de voz")
        await self.voice.connect()

        logger.info("Arrancando loops de conversación (send/receive/playback)")
        self._tasks = [
            asyncio.create_task(self._send_loop(), name="conversation-send"),
            asyncio.create_task(self._receive_loop(), name="conversation-receive"),
            asyncio.create_task(
                self._playback_loop(), name="conversation-playback-loop"
            ),
        ]

        try:
            await asyncio.gather(*self._tasks)
        except asyncio.CancelledError:
            logger.debug("Loops de conversación cancelados")
        except Exception:
            logger.exception("Error inesperado en la conversación")
            raise

    async def stop(self) -> None:
        """Corta la conversación: cancela las tareas y libera audio y voz."""
        logger.info("Deteniendo conversación")

        if self._playback_task is not None:
            self._playback_task.cancel()

        for task in self._tasks:
            task.cancel()
        for task in self._tasks:
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._tasks = []

        await self.voice.disconnect()
        logger.info("Conversación detenida")

    async def _send_loop(self) -> None:
        """Lee audio del micrófono y lo manda al proveedor de voz."""
        try:
            while True:
                chunk = await self.audio.read_chunk()
                logger.debug("Chunk leído del micrófono (%d bytes)", len(chunk))
                await self.voice.send_audio(chunk)
        except Exception:
            logger.exception("Error en send_loop (micrófono → voice)")
            raise

    async def _receive_loop(self) -> None:
        """Recibe eventos del proveedor de voz e interpreta qué
        significan. A propósito NO reproduce audio directamente —
        solo lo encola para _playback_loop. Así, este loop nunca
        queda bloqueado esperando que suene un chunk, y puede
        reaccionar a "interrupted" apenas lo recibe, sin importar
        cuánto audio haya todavía pendiente de sonar.
        """
        try:
            async for kind, payload in self.voice.receive():
                if kind == "interrupted":
                    pending = self._playback_queue.qsize()
                    logger.info(
                        "Interrupción detectada (barge-in) — cortando reproducción "
                        "y descartando %d chunk(s) pendiente(s)",
                        pending,
                    )
                    self._clear_playback_queue()
                    if self._playback_task is not None:
                        self._playback_task.cancel()
                    await self.voice.interrupt()
                    continue

                if kind == "audio":
                    logger.debug(
                        "Chunk recibido de voice, encolado para reproducir (%d bytes)",
                        len(payload),
                    )
                    await self._playback_queue.put(payload)
        except Exception:
            logger.exception("Error en receive_loop (voice → cola de reproducción)")
            raise

    async def _playback_loop(self) -> None:
        """Consume la cola de audio y lo reproduce en orden, un chunk
        a la vez. Vive separado de _receive_loop para que recibir
        eventos nunca dependa de cuánto tarda en sonar el audio.
        """
        try:
            while True:
                payload = await self._playback_queue.get()
                self._playback_task = asyncio.create_task(
                    self.audio.write_chunk(payload), name="conversation-playback"
                )
                try:
                    await self._playback_task
                except asyncio.CancelledError:
                    pass
                finally:
                    self._playback_task = None
        except Exception:
            logger.exception("Error en playback_loop (cola → parlantes)")
            raise

    def _clear_playback_queue(self) -> None:
        """Descarta cualquier audio todavía no reproducido — se usa
        al interrumpir, para no seguir reproduciendo una respuesta
        que Gemini ya abandonó.
        """
        while not self._playback_queue.empty():
            try:
                self._playback_queue.get_nowait()
            except asyncio.QueueEmpty:
                break
