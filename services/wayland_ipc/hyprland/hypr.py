from ignis.services.hyprland import HyprlandService
from services.wayland_ipc.hyprland import (
    HyprWorkspace,
    HyprWindows,
    HyprMonitors,
    HyprMainKeyboard,
)
from services.wayland_ipc.interfaces import (
    IWaylandIpc,
    IWindows,
    IWorkspace,
    IMonitors,
    IMainKeyboard,
)


class Hypr(IWaylandIpc):
    """
    Hyprland ipc
    """

    def __init__(self):
        self.hypr = HyprlandService.get_default()

    def workspace(self) -> IWorkspace:
        """
        Return a dictionary of workspaces.
        """
        return HyprWorkspace(self)

    def windows(self) -> IWindows:
        """
        Return a list of windows as WindowsModel instances.
        """
        return HyprWindows(self)

    def monitors(self) -> IMonitors:
        """
        Return a list of monitors as MonitorsModel instances.
        """
        return HyprMonitors(self)

    def main_keyboard(self) -> IMainKeyboard:
        """
        Return the main keyboard as a dictionary.
        """
        return HyprMainKeyboard(self)
