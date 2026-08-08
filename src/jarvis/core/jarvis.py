from jarvis.voice.provider import VoiceProvider


class Jarvis:
    def __init__(
        self,
        voice: VoiceProvider,
        reasoning=None,
        memory=None,
        tools=None,
    ):
        self.voice = voice
        self.reasoning = reasoning
        self.memory = memory
        self.tools = tools

    async def start(self) -> None:
        await self.voice.connect()
