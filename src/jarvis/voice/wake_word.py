from abc import ABC, abstractmethod

from jarvis.audio.io import AudioIO


class WakeWordProvider(ABC):
    """Detecta la palabra de activación de JARVIS.

    No abre ni cierra el micrófono — recibe una instancia de AudioIO
    ya abierta (la misma que usa el resto del sistema, para no
    competir por el hardware) y lee de ahí hasta detectar la wake
    word, momento en el que retorna. No es un generador infinito:
    una llamada = una espera = una detección.
    """

    @abstractmethod
    async def connect(self) -> None:
        """Carga el modelo de detección en memoria."""
        ...

    @abstractmethod
    async def disconnect(self) -> None:
        """Libera el modelo de detección."""
        ...

    @abstractmethod
    async def listen_until_detected(self, audio: AudioIO) -> None:
        """Lee chunks de audio de `audio` y evalúa cada uno contra el
        modelo cargado. No retorna hasta detectar la palabra de
        activación — es la espera bloqueante (a nivel de lógica, no
        de threads) que el orquestador necesita antes de arrancar
        una conversación.
        """
        ...
