from loguru import logger
from ignis.app import IgnisApp
from .widgets_list import WidgetsList


class InitWidgets:
    def __init__(self):
        self.app = IgnisApp()

    def init(self):
        logger.info("Initializing widgets...")
        for widget in WidgetsList.WIDGETS:
            widget()

    def run(self):
        self.app.connect("activate", lambda _: self.init())
        self.app.run(None)
