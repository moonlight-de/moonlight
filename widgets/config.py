from utils import ConfigManager
from services import WaylandIpcHandler


class ConfigWidgetManager(ConfigManager):
    """
    Initialize the config manager
    """

    def __init__(self) -> None:
        super().__init__()
        self.wayland_ipc = WaylandIpcHandler.create_wayland_ipc()

        self.general = self.cfg.general
        self.widgets = self.cfg.widgets
        self.statusbar = self.cfg.widgets.statusbar


config_manager = ConfigWidgetManager()
