from logtail import LogtailHandler
import logging

try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings

handler = LogtailHandler(source_token=f"{settings.BETTERSTACK_SOURCE_TOKEN}")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(handler)
