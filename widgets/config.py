from utils.configuration_manager import ConfigManager
from utils.tools import PositionHandler
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

        self.statusbar_is_vertical = PositionHandler.statusbar_is_vertical(
            self.statusbar.position.value
        )


config_manager = ConfigWidgetManager()
