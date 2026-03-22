from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.models import WorkspaceModel


class IWorkspace(ABC):
    """
    Interface for workspaces
    """

    @property
    @abstractmethod
    def list_workspaces(self) -> dict[int, "WorkspaceModel"]:
        """
        Return a dictionary of workspaces.

        Returns:
            dict[int, WorkspaceModel]: Mapping workspace ID -> workspace info.

        Example:
            {
                1: WorkspaceModel(
                    name="1",
                    monitor="eDP-1",
                    monitor_id=0,
                    windows=1,
                    fullscreen=False
                ),
                2: WorkspaceModel(...),
                -98: WorkspaceModel(...),
            }
        """
        ...

    @property
    @abstractmethod
    def active_workspace_id(self) -> int:
        """
        Return the ID of the active workspace.

        Returns:
            int: Workspace ID

        Example:
            1

        Usage with `list_workspaces`:
            ws_dict = instance.list_workspaces()
            active_ws = ws_dict[instance.active_workspace_id()]
            print(active_ws.name)
        """
        ...

    @abstractmethod
    def refresh(self) -> None:
        """
        Refresh the list of workspaces.
        """
