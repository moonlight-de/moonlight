from ignis.services.hyprland import HyprlandService
from ignis.gobject import IgnisProperty

from .workspace import HyprWorkspace
from .windows import HyprWindows
from .monitors import HyprMonitors
from .main_keyboard import HyprMainKeyboard

from services.wayland_ipc.interfaces import (
    IWaylandIpc,
    IWindows,
    IWorkspace,
    IMonitors,
    IMainKeyboard,
)


class Hyprctl(IWaylandIpc):
    """
    Hyprland IPC
    """

    @staticmethod
    def name() -> str:
        return "hyprland"

    def __init__(self):
        self.hypr = HyprlandService.get_default()

    def workspace(self) -> IWorkspace:
        return HyprWorkspace(self)

    def windows(self) -> IWindows:
        return HyprWindows(self)

    def monitors(self) -> IMonitors:
        return HyprMonitors(self)

    def main_keyboard(self) -> IMainKeyboard:
        return HyprMainKeyboard(self)
