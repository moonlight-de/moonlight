from services.wayland_ipc.hyprland.models import WorkspaceModel
from services.wayland_ipc.interfaces import IWorkspace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.hypr import Hyprctl


class HyprWorkspace(IWorkspace):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    def list_workspaces(self) -> dict[int, WorkspaceModel]:
        """
        Returns a dictionary of workspace ID -> WorkspaceModel
        """
        list_ws: dict[int, WorkspaceModel] = {}
        for ws in self.hyprland_ipc.hypr.workspaces:
            list_ws[ws.id] = WorkspaceModel(
                name=ws.name,
                monitor=ws.monitor,
                monitor_id=ws.monitor_id,
                windows=ws.windows,
                has_fullscreen=ws.has_fullscreen,
            )
        return list_ws

    def active_workspace_id(self) -> int:
        """
        Returns the ID of the currently active workspace
        """
        return self.hyprland_ipc.hypr.active_workspace.id
