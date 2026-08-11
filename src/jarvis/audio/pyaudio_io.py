import asyncio
import logging

import pyaudio

from jarvis.audio.io import AudioIO

logger = logging.getLogger(__name__)

FORMAT = pyaudio.paInt16
CHANNELS = 1
SEND_SAMPLE_RATE = 16000
RECEIVE_SAMPLE_RATE = 24000
CHUNK_SIZE = 1024


class PyAudioIO(AudioIO):
    """Implementación concreta de AudioIO usando PyAudio.

    Responsabilidad única: hablar con el hardware de audio local
    (micrófono y parlantes). No sabe nada de Gemini, de JARVIS ni
    de cómo se orquesta una conversación.
    """

    def __init__(self):
        self._pya: pyaudio.PyAudio | None = None
        self._input_stream: pyaudio.Stream | None = None
        self._output_stream: pyaudio.Stream | None = None

    async def start(self) -> None:
        logger.info("Iniciando PyAudio")
        self._pya = pyaudio.PyAudio()

        try:
            mic_info = self._pya.get_default_input_device_info()
        except OSError:
            logger.exception(
                "No se encontró un dispositivo de entrada de audio por defecto"
            )
            raise

        logger.info(
            "Dispositivo de entrada: %s (index=%s)", mic_info["name"], mic_info["index"]
        )

        self._input_stream = await asyncio.to_thread(
            self._pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=SEND_SAMPLE_RATE,
            input=True,
            input_device_index=mic_info["index"],
            frames_per_buffer=CHUNK_SIZE,
        )

        self._output_stream = await asyncio.to_thread(
            self._pya.open,
            format=FORMAT,
            channels=CHANNELS,
            rate=RECEIVE_SAMPLE_RATE,
            output=True,
        )
        logger.info(
            "Streams de audio abiertos (input=%dHz, output=%dHz)",
            SEND_SAMPLE_RATE,
            RECEIVE_SAMPLE_RATE,
        )

    async def stop(self) -> None:
        logger.info("Deteniendo PyAudio")

        if self._input_stream is not None:
            await asyncio.to_thread(self._input_stream.close)
            self._input_stream = None

        if self._output_stream is not None:
            await asyncio.to_thread(self._output_stream.close)
            self._output_stream = None

        if self._pya is not None:
            await asyncio.to_thread(self._pya.terminate)
            self._pya = None

        logger.info("PyAudio detenido")

    async def read_chunk(self) -> bytes:
        assert self._input_stream is not None, (
            "AudioIO no fue iniciado (llamar start() primero)"
        )
        try:
            return await asyncio.to_thread(
                self._input_stream.read, CHUNK_SIZE, exception_on_overflow=False
            )
        except Exception:
            logger.exception("Error leyendo audio del micrófono")
            raise

    async def write_chunk(self, data: bytes) -> None:
        assert self._output_stream is not None, (
            "AudioIO no fue iniciado (llamar start() primero)"
        )
        try:
            await asyncio.to_thread(self._output_stream.write, data)
        except Exception:
            logger.exception("Error escribiendo audio a los parlantes")
            raise
