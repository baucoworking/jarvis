import logging
import os

import numpy as np
import openwakeword.utils
from dotenv import load_dotenv
from openwakeword.model import Model

from jarvis.audio.io import AudioIO
from jarvis.voice.wake_word import WakeWordProvider

load_dotenv()  # Carga variables de entorno desde .env

WAKE_WORD_MODEL_PATH = os.getenv("WAKE_WORD_MODEL_PATH")
DETECTION_THRESHOLD = 0.5

logger = logging.getLogger(__name__)


class OpenWakeWordProvider(WakeWordProvider):
    def __init__(self):
        self.model: Model | None = None

    async def connect(self) -> None:
        openwakeword.utils.download_models()
        self.model = Model(
            wakeword_models=[WAKE_WORD_MODEL_PATH],
            inference_framework="onnx",
        )

    async def disconnect(self) -> None:
        self.model = None

    async def listen_until_detected(self, audio: AudioIO) -> None:
        assert self.model is not None, (
            "OpenWakeWordProvider no está conectado (llamar connect() primero)"
        )

        logger.info("Escuchando wake word... decí 'Jarvis' (Ctrl+C para salir)")

        while True:
            chunk = await audio.read_chunk()
            samples = np.frombuffer(chunk, dtype=np.int16)
            prediction = self.model.predict(samples)

            if any(score >= DETECTION_THRESHOLD for score in prediction.values()):
                return
