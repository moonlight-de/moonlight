from typing import TYPE_CHECKING, Callable

from services.wayland_ipc.interfaces import IMonitorEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.events import HyprEvents


class MonitorEvent(IMonitorEvent):
    def __init__(self, hypr_events: "HyprEvents") -> None:
        self.hypr_events = hypr_events

    def moved(self, callback: Callable) -> None:
        self.hypr_events.on("monitorremovedv2", callback)

    def added(self, callback: Callable) -> None:
        self.hypr_events.on("monitoraddedv2", callback)

    def removed(self, callback: Callable) -> None:
        self.hypr_events.on("monitorremovedv2", callback)
