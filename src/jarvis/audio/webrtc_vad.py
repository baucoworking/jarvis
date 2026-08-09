import webrtcvad

from jarvis.audio.vad import VoiceActivityDetector

# webrtcvad solo acepta frames de 10, 20 o 30 ms exactos.
# El resto del sistema usa chunks más grandes (CHUNK_SIZE en
# pyaudio_io.py), así que cada chunk se trocea internamente en
# sub-frames de este tamaño antes de analizarlos.
_FRAME_DURATION_MS = 30

# Agresividad del filtro: 0 (menos agresivo, más permisivo con
# ruido) a 3 (más agresivo, filtra más No-voz). 3 reduce falsos
# positivos por ruido de fondo (ideal para no disparar barge-in
# con cualquier ruido).
_AGGRESSIVENESS = 3


class WebRtcVAD(VoiceActivityDetector):
    """Implementación concreta de VoiceActivityDetector usando
    webrtcvad (el detector de voz de Google usado en WebRTC).

    Responsabilidad única: decidir si un chunk de audio contiene
    voz humana. No sabe nada de Gemini, de JARVIS ni de cómo se
    usa ese resultado.
    """

    def __init__(self, aggressiveness: int = _AGGRESSIVENESS):
        self._vad = webrtcvad.Vad(aggressiveness)

    def is_speech(self, chunk: bytes, sample_rate: int) -> bool:
        frame_size = (
            int(sample_rate * _FRAME_DURATION_MS / 1000) * 2
        )  # 2 bytes/muestra (16-bit)

        for start in range(0, len(chunk) - frame_size + 1, frame_size):
            frame = chunk[start : start + frame_size]
            if self._vad.is_speech(frame, sample_rate):
                return True

        return False
