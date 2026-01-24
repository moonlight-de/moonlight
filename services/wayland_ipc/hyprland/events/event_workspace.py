from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from services.wayland_ipc.interfaces import IWorkspaceEvent
from .hyprland_event import HyprlandEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.events import HyprEvents


class WorkspaceEvent(IWorkspaceEvent):
    def __init__(self, hypr_events: HyprEvents) -> None:
        self.hypr_events = hypr_events

    def changed(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.WORKSPACE_V2, callback)

    def created(self, callback) -> None:
        self.hypr_events.on(HyprlandEvent.CREATE_WORKSPACE_V2, callback)

    def destroyed(self, callback: Callable) -> None:
        self.hypr_events.on(HyprlandEvent.DESTROY_WORKSPACE_V2, callback)

    def moved(self, callback: Callable):
        self.hypr_events.on(HyprlandEvent.MOVE_WORKSPACE_V2, callback)

    def renamed(self, callback: Callable):
        self.hypr_events.on(HyprlandEvent.RENAME_WORKSPACE, callback)
