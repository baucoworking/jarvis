import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from jarvis.voice.provider import VoiceProvider

load_dotenv()

logger = logging.getLogger(__name__)


MODEL = "models/gemini-3.1-flash-live-preview"

SYSTEM_INSTRUCTION_PATH = (
    Path(__file__).parent.parent / "prompts" / "system_instruction.md"
)


def load_system_instruction() -> str:
    return SYSTEM_INSTRUCTION_PATH.read_text(encoding="utf-8")


class GeminiLiveProvider(VoiceProvider):
    def __init__(self):
        self.client = genai.Client(
            http_options={"api_version": "v1beta"},
            api_key=os.environ.get("GEMINI_API_KEY"),
        )

        self.config = types.LiveConnectConfig(
            response_modalities=["AUDIO"],
            system_instruction=load_system_instruction(),
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
        self.system_instruction = load_system_instruction()

    async def connect(self) -> None:
        logger.info("Conectando a Gemini Live (modelo=%s)", MODEL)
        try:
            self._session_cm = self.client.aio.live.connect(
                model=MODEL, config=self.config
            )
            self.session = await self._session_cm.__aenter__()
        except Exception:
            logger.exception("Error conectando a Gemini Live")
            raise
        logger.info("Conectado a Gemini Live")

    async def disconnect(self) -> None:
        if self._session_cm is not None:
            logger.info("Desconectando de Gemini Live")
            await self._session_cm.__aexit__(None, None, None)
            self._session_cm = None
            self.session = None

    async def send_audio(self, audio: bytes) -> None:
        logger.debug("Enviando audio a Gemini (%d bytes)", len(audio))
        assert self.session is not None, (
            "GeminiLiveProvider no está conectado (llamar connect() primero)"
        )
        await self.session.send_realtime_input(
            audio=types.Blob(data=audio, mime_type="audio/pcm;rate=16000")
        )

    async def receive(self):
        """Async generator: yields eventos a medida que Gemini los va
        generando. Cada evento es una tupla (tipo, payload):
          ("audio", bytes)  -> chunk de audio para reproducir
          ("interrupted", None) -> el servidor detectó que el usuario
              habló durante la generación (barge-in nativo). Quien
              consuma este generador debe cortar la reproducción en
              curso al recibir esto.
        """
        assert self.session is not None, (
            "GeminiLiveProvider no está conectado (llamar connect() primero)"
        )
        while True:
            turn = self.session.receive()
            async for response in turn:
                server_content = response.server_content
                if server_content is not None and server_content.interrupted:
                    logger.debug("Gemini señalizó interrupción (barge-in nativo)")
                    yield ("interrupted", None)
                    continue

                if data := response.data:
                    logger.debug("Audio recibido de Gemini (%d bytes)", len(data))
                    yield ("audio", data)

    async def interrupt(self) -> None:
        """No-op: con el VAD automático del servidor (config por
        defecto), Gemini detecta y corta la interrupción por su
        cuenta — no hace falta que JARVIS le avise nada. Se mantiene
        en la interfaz porque Conversation la llama al recibir
        ("interrupted", None) desde receive(), pero para este
        proveedor no hay nada que enviar.
        """
