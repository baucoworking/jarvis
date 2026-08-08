import asyncio

from jarvis.audio.pyaudio_io import PyAudioIO
from jarvis.core.jarvis import Jarvis
from jarvis.voice.gemini_live import GeminiLiveProvider


async def main() -> None:
    voice = GeminiLiveProvider()
    audio = PyAudioIO()
    jarvis = Jarvis(voice=voice, audio=audio)

    await jarvis.start()


def run() -> None:
    """Entry point sincrónico: lo que invoca `uv run jarvis`.
    Su única responsabilidad es arrancar el event loop.
    """
    asyncio.run(main())


if __name__ == "__main__":
    run()
