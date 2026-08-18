import asyncio
import logging

from jarvis.audio.pyaudio_io import PyAudioIO
from jarvis.core.jarvis import Jarvis
from jarvis.logging_config import setup_logging
from jarvis.voice.gemini_live import GeminiLiveProvider
from jarvis.voice.openww import OpenWakeWordProvider

logger = logging.getLogger(__name__)


async def main() -> None:
    voice = GeminiLiveProvider()
    audio = PyAudioIO()
    wake_word = OpenWakeWordProvider()
    jarvis = Jarvis(voice=voice, audio=audio, wake_word=wake_word)

    logger.info("JARVIS arrancando")
    try:
        await jarvis.start()
    finally:
        logger.info("JARVIS finalizado")


def run() -> None:
    """Entry point sincrónico: lo que invoca `uv run jarvis`.
    Configura logging y arranca el event loop.
    """
    setup_logging()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrumpido por el usuario (Ctrl+C)")


if __name__ == "__main__":
    run()
