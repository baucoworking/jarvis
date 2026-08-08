from abc import ABC, abstractmethod


class AudioIO(ABC):
    """Capacidad de audio que JARVIS necesita: leer del micrófono y
    escribir a los parlantes. No sabe nada de Gemini ni de JARVIS —
    solo mueve bytes crudos de audio hacia y desde el hardware.
    """

    @abstractmethod
    async def start(self) -> None:
        """Abre los streams de entrada y salida."""
        ...

    @abstractmethod
    async def stop(self) -> None:
        """Cierra los streams y libera el hardware."""
        ...

    @abstractmethod
    async def read_chunk(self) -> bytes:
        """Lee un chunk de audio crudo desde el micrófono."""
        ...

    @abstractmethod
    async def write_chunk(self, data: bytes) -> None:
        """Reproduce un chunk de audio crudo por los parlantes."""
        ...
