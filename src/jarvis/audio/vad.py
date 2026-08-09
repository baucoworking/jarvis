from abc import ABC, abstractmethod


class VoiceActivityDetector(ABC):
    """Capacidad de detectar si un chunk de audio contiene voz humana.

    No sabe nada de PyAudio, de Gemini ni de cómo se orquesta la
    conversación — solo analiza bytes de audio crudo y responde
    sí/no hay voz. Es la pieza que le permite a Conversation saber
    "el usuario empezó a hablar" sin depender de lo que diga el
    servidor de Gemini.
    """

    @abstractmethod
    def is_speech(self, chunk: bytes, sample_rate: int) -> bool:
        """Analiza un chunk de audio PCM y determina si contiene voz."""
        ...
