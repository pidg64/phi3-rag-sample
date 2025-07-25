# utils/logger.py

import sys
import logging
from app.core.settings import settings


def setup_logger():
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format='%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    if not settings.DEBUG:
        for noisy_logger in [
            'httpx',
            'httpcore',
            'openai',
            'urllib3',
            'requests',
            'sentence_transformers',
            'transformers',
        ]:
            logging.getLogger(noisy_logger).setLevel(logging.WARNING)
            logging.getLogger(noisy_logger).propagate = False

    return logging.getLogger(__name__)

logger = setup_logger()
logger.debug('Logger configured with level: %s', 'DEBUG' if settings.DEBUG else 'INFO')