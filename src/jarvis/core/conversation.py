import asyncio

from jarvis.audio.io import AudioIO
from jarvis.voice.provider import VoiceProvider


class Conversation:
    """Orquesta una conversación de voz continua entre el hardware de
    audio (AudioIO) y el proveedor de voz (VoiceProvider).

    No sabe que el audio viene de PyAudio ni que la voz la genera
    Gemini — solo mueve bytes entre ambas abstracciones. Esa es la
    única responsabilidad de esta clase: el ciclo de vida de la
    conversación (cuándo escuchar, cuándo mandar, cuándo reproducir).

    Todavía no maneja interrupciones (barge-in): eso queda para
    después de v0.2.0.
    """

    def __init__(self, audio: AudioIO, voice: VoiceProvider):
        self.audio = audio
        self.voice = voice
        self._tasks: list[asyncio.Task] = []

    async def start(self) -> None:
        """Conecta el proveedor de voz, abre el audio, y arranca las
        dos tareas concurrentes que sostienen la conversación:
        micrófono → voice, y voice → parlantes.
        """
        await self.voice.connect()
        await self.audio.start()

        self._tasks = [
            asyncio.create_task(self._send_loop(), name="conversation-send"),
            asyncio.create_task(self._receive_loop(), name="conversation-receive"),
        ]

        try:
            await asyncio.gather(*self._tasks)
        except asyncio.CancelledError:
            pass

    async def stop(self) -> None:
        """Corta la conversación: cancela las tareas y libera audio y voz."""
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

    async def _send_loop(self) -> None:
        """Lee audio del micrófono y lo manda al proveedor de voz."""
        while True:
            chunk = await self.audio.read_chunk()
            await self.voice.send_audio(chunk)

    async def _receive_loop(self) -> None:
        """Recibe audio del proveedor de voz y lo reproduce."""
        async for chunk in self.voice.receive():
            await self.audio.write_chunk(chunk)
