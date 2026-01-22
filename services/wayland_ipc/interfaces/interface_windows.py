from abc import ABC, abstractmethod
from typing import List
from services.wayland_ipc.hyprland.models import WindowsModel


class IWindows(ABC):
    """
    Interface for interacting with windows.
    """

    @abstractmethod
    def list_windows(self) -> List[WindowsModel]:
        """
        Return a list of windows as WindowsModel instances.

        Example:
            [
                WindowsModel(
                    address="0x558c8deb0f40",
                    at=[17, 17],
                    size=[1280, 720],
                    workspace_id=1,
                    floating=True,
                    monitor="eDP-1",
                    monitor_id=0,
                    class_name="firefox",
                    title="Mozilla Firefox ...",
                    initial_title="Firefox",
                    pid=1234,
                    pinned=False,
                    fullscreen=False,
                ),
                ...
            ]
        """
        ...

    @abstractmethod
    def list_windows_on_workspace(self, workspace_id: int) -> List[WindowsModel]:
        """
        Return a list of windows on a workspace as WindowsModel instances.

        Example:
            list_ws = list_windows_on_workspace(3)
            print(list_ws)
        """
        ...

    @abstractmethod
    def get_window_by_address(self, address: str) -> WindowsModel | None:
        """
        Return a specific window by its unique address, or None if not found.

        Args:
            address: The address of the window (e.g., "0x558c8deb0f40").
        """
        ...
