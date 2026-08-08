from jarvis.core.jarvis import Jarvis
from jarvis.voice.gemini_live import GeminiLiveProvider


def main() -> None:
    voice = GeminiLiveProvider()
    jarvis = Jarvis(voice=voice)
    jarvis.start()


if __name__ == "__main__":
    main()
