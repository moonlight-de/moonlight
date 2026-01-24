from typing import TYPE_CHECKING, Optional, Callable, Any

from utils.constants.supported_desktops import SupportedDesktops
from .ipc_listener import HyprlandIPCListener

from services.wayland_ipc.interfaces import (
    IEvents,
    IWorkspaceEvent,
    IWindowEvent,
    IMonitorEvent,
    IMainKeyboardEvent,
)

from .event_workspace import WorkspaceEvent
from .event_window import WindowEvent
from .event_monitor import MonitorEvent
from .event_main_keyboard import MainKeyboardEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprEvents(IEvents):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

        socket2 = SupportedDesktops.HYPR_SOCKET_DIR / ".socket2.sock"
        self._listener = HyprlandIPCListener(socket2)

        self._callbacks: dict[str, list[Callable[[], None]]] = {}

        self._workspace: Optional[WorkspaceEvent] = None
        self._window: Optional[WindowEvent] = None
        self._main_keyboard: Optional[MainKeyboardEvent] = None
        self._monitor: Optional[MonitorEvent] = None

        self._listener.connect("raw-event", self.__dispatch)
        self._listener.start()

    def on(self, event: str, callback: Callable) -> None:
        self._callbacks.setdefault(event.lower(), []).append(callback)

    @property
    def workspace(self) -> IWorkspaceEvent:
        if self._workspace is None:
            self._workspace = WorkspaceEvent(self)
        return self._workspace

    @property
    def window(self) -> IWindowEvent:
        if self._window is None:
            self._window = WindowEvent(self)
        return self._window

    @property
    def main_keyboard(self) -> IMainKeyboardEvent:
        if self._main_keyboard is None:
            self._main_keyboard = MainKeyboardEvent(self)
        return self._main_keyboard

    @property
    def monitor(self) -> "IMonitorEvent":
        if self._monitor is None:
            self._monitor = MonitorEvent(self)
        return self._monitor

    def __dispatch(self, _listener, event: str, payload: str) -> None:
        for cb in self._callbacks.get(event.lower(), []):
            try:
                cb()
            except Exception as e:
                import logging

                logging.exception("Error in Hyprland callback")
