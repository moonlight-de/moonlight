from typing import Optional
from ignis.services.hyprland import HyprlandService


from .workspace import HyprWorkspace
from .windows import HyprWindows
from .monitors import HyprMonitors
from .main_keyboard import HyprMainKeyboard
from .events import HyprEvents


from services.wayland_ipc.interfaces import (
    IWaylandIpc,
    IWindows,
    IWorkspace,
    IMonitors,
    IMainKeyboard,
    IEvents,
)


class Hyprctl(IWaylandIpc):
    """
    Hyprland IPC implementation with field-like access (no parentheses).
    Backing attrs are initialized to None and filled lazily.
    """

    def __init__(self) -> None:
        self.hypr = HyprlandService.get_default()

        # backing fields for lazy init
        self._workspace: Optional[IWorkspace] = None
        self._windows: Optional[IWindows] = None
        self._monitors: Optional[IMonitors] = None
        self._main_keyboard: Optional[IMainKeyboard] = None
        self._events: Optional[HyprEvents] = None

    @property
    def workspace(self) -> IWorkspace:
        if self._workspace is None:
            self._workspace = HyprWorkspace(self)
        return self._workspace

    @property
    def windows(self) -> IWindows:
        if self._windows is None:
            self._windows = HyprWindows(self)
        return self._windows

    @property
    def monitors(self) -> IMonitors:
        if self._monitors is None:
            self._monitors = HyprMonitors(self)
        return self._monitors

    @property
    def main_keyboard(self) -> IMainKeyboard:
        if self._main_keyboard is None:
            self._main_keyboard = HyprMainKeyboard(self)
        return self._main_keyboard

    @property
    def events(self) -> IEvents:
        if self._events is None:
            self._events = HyprEvents(self)
        return self._events
