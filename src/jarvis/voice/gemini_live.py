import os

from google import genai
from google.genai import types

from jarvis.voice.provider import VoiceProvider

MODEL = "models/gemini-3.1-flash-live-preview"


class GeminiLiveProvider(VoiceProvider):

    def __init__(self):
        self.client = genai.Client(
            http_options={"api_version": "v1beta"},
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        self.config = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name="Algenib"
            )
        )
    ),
            context_window_compression=types.ContextWindowCompressionConfig(
                trigger_tokens=104857,
                sliding_window=types.SlidingWindow(
                    target_tokens=52428
                ),
            ),
        )

        self.session = None

    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_audio(self, audio: bytes) -> None:
        ...

    async def receive(self):
        ...

    async def interrupt(self) -> None:
        ...