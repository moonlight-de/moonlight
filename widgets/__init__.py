from loguru import logger
from .config import ConfigWidgetManager

config_manager = ConfigWidgetManager()
from .status_bar import StatusBar

__all__ = [
    "config_manager",
    "StatusBar",
]


def init():
    logger.info("Initializing widgets...")
    StatusBar()
