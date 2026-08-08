import asyncio

from jarvis.audio.io import AudioIO
from jarvis.core.conversation import Conversation
from jarvis.voice.provider import VoiceProvider


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
        try:
            await self.conversation.start()
        except (asyncio.CancelledError, KeyboardInterrupt):
            pass
        finally:
            await self.stop()

    async def stop(self) -> None:
        await self.conversation.stop()
