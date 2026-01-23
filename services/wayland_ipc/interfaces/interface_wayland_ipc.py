from abc import ABC, abstractmethod


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from services.wayland_ipc.interfaces import (
        IWorkspace,
        IWindows,
        IMonitors,
        IMainKeyboard,
    )


class IWaylandIpc(ABC):
    """
    Interface for wayland ipc
    """

    @staticmethod
    @abstractmethod
    def name() -> str:
        """
        Return the name of the wayland ipc
        """
        ...

    @abstractmethod
    def workspace(self) -> "IWorkspace":
        """
        Return a dictionary of workspaces.
        """
        ...

    @abstractmethod
    def windows(self) -> "IWindows":
        """
        Return a list of windows as WindowsModel instances.
        """
        ...

    @abstractmethod
    def monitors(self) -> "IMonitors":
        """
        Return a list of monitors as MonitorsModel instances.
        """

        ...

    @abstractmethod
    def main_keyboard(self) -> "IMainKeyboard":
        """
        Return the main keyboard as a dictionary.
        """

        ...
