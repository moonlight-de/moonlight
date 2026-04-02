from __future__ import annotations

from typing import TYPE_CHECKING

from services.wayland_ipc.hyprland.models import WorkspaceModel
from services.wayland_ipc.interfaces import IWorkspace

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprWorkspace(IWorkspace):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
    def list_workspaces(self) -> dict[int, WorkspaceModel]:
        return {
            ws.id: WorkspaceModel(
                name=ws.name,
                monitor=ws.monitor,
                monitor_id=ws.monitor_id,
                windows=ws.windows,
                has_fullscreen=ws.has_fullscreen,
            )
            for ws in self.hyprland_ipc.hypr.workspaces
        }

    @property
    def active_workspace_id(self) -> int:
        return self.hyprland_ipc.hypr.active_workspace.id

    def refresh(self) -> None:
        self.hyprland_ipc._refresh_workspaces()
