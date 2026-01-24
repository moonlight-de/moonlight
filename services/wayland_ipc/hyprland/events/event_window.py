from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable

from services.wayland_ipc.interfaces import IWindowEvent
from .hyprland_event import HyprlandEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.events import HyprEvents


class WindowEvent(IWindowEvent):
    def __init__(self, hypr_events: HyprEvents) -> None:
        self.hypr_events = hypr_events

    def opened(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.OPEN_WINDOW, callback)

    def closed(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.CLOSE_WINDOW, callback)

    def focus_changed(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.ACTIVE_WINDOW, callback)

    def moved(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.MOVE_WINDOW_V2, callback)

    def floating_changed(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.CHANGE_FLOATING_MODE, callback)

    def fullscreen_changed(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.FULLSCREEN, callback)
