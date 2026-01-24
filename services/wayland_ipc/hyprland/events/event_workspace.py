from typing import TYPE_CHECKING, Callable

from services.wayland_ipc.interfaces import IWorkspaceEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.events import HyprEvents


class WorkspaceEvent(IWorkspaceEvent):
    def __init__(self, hypr_events: "HyprEvents") -> None:
        self.hypr_events = hypr_events

    def changed(self, callback: Callable) -> None:
        self.hypr_events.on("workspacev2", callback)

    def created(self, callback) -> None:
        self.hypr_events.on("createworkspacev2", callback)

    def destroyed(self, callback: Callable) -> None:
        self.hypr_events.on("destroyworkspacev2", callback)

    def moved(self, callback: Callable):
        self.hypr_events.on("moveworkspacev2", callback)

    def renamed(self, callback: Callable):
        self.hypr_events.on("renameworkspace", callback)
