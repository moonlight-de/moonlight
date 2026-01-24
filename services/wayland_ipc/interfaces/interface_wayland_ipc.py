from __future__ import annotations

from abc import ABC, abstractmethod

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from services.wayland_ipc.interfaces import (
        IWorkspace,
        IWindows,
        IMonitors,
        IMainKeyboard,
        IEvents,
    )


class IWaylandIpc(ABC):
    """
    Interface for wayland ipc
    """

    @property
    @abstractmethod
    def workspace(self) -> IWorkspace:
        """
        Return a dictionary of workspaces.
        """
        ...

    @property
    @abstractmethod
    def windows(self) -> IWindows:
        """
        Return a list of windows as WindowsModel instances.
        """
        ...

    @property
    @abstractmethod
    def monitors(self) -> IMonitors:
        """
        Return a list of monitors as MonitorsModel instances.
        """

        ...

    @property
    @abstractmethod
    def main_keyboard(self) -> IMainKeyboard:
        """
        Return the main keyboard as a dictionary.
        """

        ...

    @property
    @abstractmethod
    def events(self) -> IEvents:
        """
        Return None
        ---
        for connect desktop environment events
        """
        ...
