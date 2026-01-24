from typing import TYPE_CHECKING, Any, Callable

from services.wayland_ipc.interfaces import IWindowEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.events import HyprEvents


class WindowEvent(IWindowEvent):
    def __init__(self, hypr_events: "HyprEvents") -> None:
        self.hypr_events = hypr_events

    def opened(self, callback: Callable) -> None:
        self.hypr_events.on("openwindow", callback)

    def closed(self, callback: Callable) -> None:
        self.hypr_events.on("closewindow", callback)

    def focus_changed(self, callback: Callable) -> None:
        self.hypr_events.on("activewindow", callback)

    def moved(self, callback: Callable) -> None:
        self.hypr_events.on("movewindowv2", callback)

    def floating_changed(self, callback: Callable) -> None:
        self.hypr_events.on("changefloatingmode", callback)

    def fullscreen_changed(self, callback: Callable) -> None:
        self.hypr_events.on("fullscreen", callback)
