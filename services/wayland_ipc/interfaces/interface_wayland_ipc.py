from abc import ABC, abstractmethod

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

    @abstractmethod
    def workspace(self) -> IWorkspace: ...

    @abstractmethod
    def windows(self) -> IWindows: ...

    @abstractmethod
    def monitors(self) -> IMonitors: ...

    @abstractmethod
    def main_keyboard(self) -> IMainKeyboard: ...
