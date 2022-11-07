import logging
from typing import Optional

from tests.functional.settings import get_settings

logger: Optional[logging.Logger] = None
conf = get_settings()


def init_logger():
    """Инициализирует логгер приложения."""
    global logger

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(conf.LOG_LEVEL)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def get_logger() -> logging.Logger:
    """Возвращает экземпляр логгера приложения.

    Returns:
        logging.Logger - экземпляр логгера
    """
    if not logger:
        init_logger()

    return logger
