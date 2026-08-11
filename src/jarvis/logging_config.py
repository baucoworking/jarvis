import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "jarvis.log"

# Cuántos días de logs pasados conservar antes de borrar los más viejos.
BACKUP_DAYS = 7


def setup_logging(level: int = logging.INFO) -> None:
    """Configura el logging de todo JARVIS. Se llama una sola vez,
    al arrancar el programa (en main.py) — ningún otro módulo
    configura logging, solo piden su propio logger con
    logging.getLogger(__name__) y lo usan.

    Consola: mensajes simples y legibles, para seguir la ejecución
    en vivo mientras se trabaja.

    Archivo (logs/jarvis.log): mensajes con más detalle (módulo,
    línea), rotado automáticamente cada medianoche, conservando los
    últimos BACKUP_DAYS días — evita que el archivo crezca sin
    límite, siguiendo la práctica estándar de logging en procesos
    de larga duración.
    """
    LOG_DIR.mkdir(exist_ok=True)

    root_logger = logging.getLogger("jarvis")
    root_logger.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s", datefmt="%H:%M:%S"
        )
    )

    file_handler = TimedRotatingFileHandler(
        LOG_FILE, when="midnight", backupCount=BACKUP_DAYS, encoding="utf-8"
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s (%(filename)s:%(lineno)d): %(message)s"
        )
    )

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
