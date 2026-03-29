from loguru import logger
from ignis.app import IgnisApp

from .widgets_list import WidgetsList
from .stylesheet.manager import StylesheetManager


class InitWidgets:
    def __init__(self):
        self.app = IgnisApp()
        self._initialized = False
        self.stylesheet_manager = StylesheetManager()

    def init(self) -> None:
        if self._initialized:
            return

        self._initialized = True
        logger.info("Initializing widgets...")

        self.stylesheet_manager.setup()

        for widget_factory in WidgetsList.WIDGETS:
            widget_factory()

    def run(self) -> None:
        self.app.connect("activate", lambda _: self.init())
        self.app.run(None)
