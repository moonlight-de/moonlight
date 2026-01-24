import json
from typing import TYPE_CHECKING
from ignis.services.hyprland import HyprlandWorkspace

from services.wayland_ipc.hyprland.models import WorkspaceModel
from services.wayland_ipc.interfaces import IWorkspace

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprWorkspace(IWorkspace):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
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

    @property
    def active_workspace_id(self) -> int:
        """
        Returns the ID of the currently active workspace
        """
        return self.hyprland_ipc.hypr.active_workspace.id

    def refresh(self) -> None:
        """
        Refresh the list of workspaces.
        """
        data_list = json.loads(self.hyprland_ipc.hypr.send_command("j/workspaces"))

        old_workspaces = self.hyprland_ipc.hypr._workspaces
        new_workspaces: dict[int, HyprlandWorkspace] = {}

        for data in data_list:
            ws_id = data["id"]

            if ws_id in old_workspaces:
                ws = old_workspaces[ws_id]
            else:
                ws = HyprlandWorkspace(self.hyprland_ipc.hypr)
                self.hyprland_ipc.hypr.emit("workspace-added", ws)

            ws.sync(data)
            new_workspaces[ws_id] = ws

        for ws_id, ws in old_workspaces.items():
            if ws_id not in new_workspaces:
                ws.emit("destroyed")

        self.hyprland_ipc.hypr._workspaces = dict(sorted(new_workspaces.items()))
