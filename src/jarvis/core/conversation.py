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
    """

    def __init__(self, audio: AudioIO, voice: VoiceProvider):
        self.audio = audio
        self.voice = voice
        self._tasks: list[asyncio.Task] = []
        self._playback_task: asyncio.Task | None = None

    async def start(self) -> None:
        """Conecta el proveedor de voz, abre el audio, y arranca las
        dos tareas concurrentes que sostienen la conversación:
        micrófono → voice, y voice → parlantes.
        """
        logger.info("Conectando proveedor de voz")
        await self.voice.connect()

        logger.info("Iniciando audio")
        await self.audio.start()

        logger.info("Arrancando loops de conversación (send/receive)")
        self._tasks = [
            asyncio.create_task(self._send_loop(), name="conversation-send"),
            asyncio.create_task(self._receive_loop(), name="conversation-receive"),
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

        await self.audio.stop()
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
        """Recibe eventos del proveedor de voz: reproduce audio, y
        corta la reproducción en curso si el proveedor señaliza una
        interrupción (barge-in detectado por su VAD nativo).
        """
        try:
            async for kind, payload in self.voice.receive():
                if kind == "interrupted":
                    logger.info(
                        "Interrupción detectada (barge-in) — cortando reproducción"
                    )
                    if self._playback_task is not None:
                        self._playback_task.cancel()
                    await self.voice.interrupt()
                    continue

                if kind == "audio":
                    logger.debug(
                        "Chunk recibido para reproducir (%d bytes)", len(payload)
                    )
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
            logger.exception("Error en receive_loop (voice → parlantes)")
            raise
