import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from jarvis.voice.provider import VoiceProvider

load_dotenv()

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
                sliding_window=types.SlidingWindow(target_tokens=52428),
            ),
        )

        self.session = None
        self._session_cm = None

    async def connect(self) -> None:
        self._session_cm = self.client.aio.live.connect(model=MODEL, config=self.config)
        self.session = await self._session_cm.__aenter__()

    async def disconnect(self) -> None:
        if self._session_cm is not None:
            await self._session_cm.__aexit__(None, None, None)
            self._session_cm = None
            self.session = None

    async def send_audio(self, audio: bytes) -> None:
        assert self.session is not None, (
            "GeminiLiveProvider no está conectado (llamar connect() primero)"
        )
        await self.session.send_realtime_input(
            audio=types.Blob(data=audio, mime_type="audio/pcm;rate=16000")
        )

    async def receive(self):
        """Async generator: yields chunks de audio (bytes) a medida que
        Gemini los va generando, turno por turno, indefinidamente.
        """
        assert self.session is not None, (
            "GeminiLiveProvider no está conectado (llamar connect() primero)"
        )
        while True:
            turn = self.session.receive()
            async for response in turn:
                if data := response.data:
                    yield data

    async def interrupt(self) -> None:
        # Gemini Live soporta barge-in nativo, pero JARVIS todavía no
        # maneja interrupciones (decisión: v0.2.0 es solo conversación
        # continua). Se deja explícito en vez de simular que funciona.
        raise NotImplementedError(
            "interrupt() todavía no está implementado (planeado post v0.2.0)"
        )
