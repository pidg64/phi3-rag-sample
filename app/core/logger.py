# utils/logger.py

import sys
import logging
from app.core.settings import settings

def setup_logger():
    if not settings.DEBUG:
        logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
        logging.getLogger("transformers").setLevel(logging.WARNING)

    logging.basicConfig(
        level=logging.DEBUG if settings.DEBUG else logging.INFO,
        format="%(message)s",
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    return logging.getLogger(__name__)
