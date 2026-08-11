from abc import ABC, abstractmethod


class VoiceProvider(ABC):
    @abstractmethod
    async def connect(self) -> None: ...

    @abstractmethod
    async def disconnect(self) -> None: ...

    @abstractmethod
    async def send_audio(self, audio: bytes) -> None: ...

    @abstractmethod
    async def receive(self): ...

    @abstractmethod
    async def interrupt(self) -> None:
        """Corta la generación en curso del proveedor de voz
        (barge-in), cuando el proveedor detecta que el usuario
        retomó la palabra.
        """
        ...
