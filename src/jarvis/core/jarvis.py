import asyncio
import logging

from jarvis.audio.io import AudioIO
from jarvis.core.conversation import Conversation
from jarvis.voice.provider import VoiceProvider

logger = logging.getLogger(__name__)


class Jarvis:
    def __init__(
        self,
        voice: VoiceProvider,
        audio: AudioIO,
        reasoning=None,
        memory=None,
        tools=None,
    ):
        self.voice = voice
        self.audio = audio
        self.reasoning = reasoning
        self.memory = memory
        self.tools = tools

        self.conversation = Conversation(audio=self.audio, voice=self.voice)

    async def start(self) -> None:
        logger.info("Iniciando JARVIS")
        try:
            await self.conversation.start()
        except (asyncio.CancelledError, KeyboardInterrupt):
            logger.info("Conversación cancelada por el usuario")
        except Exception:
            logger.exception("Error inesperado al correr la conversación")
            raise
        finally:
            await self.stop()

    async def stop(self) -> None:
        logger.info("Deteniendo JARVIS")
        await self.conversation.stop()
