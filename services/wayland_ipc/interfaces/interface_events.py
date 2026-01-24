from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .interface_workspace_event import IWorkspaceEvent
    from .interface_window_event import IWindowEvent
    from .interface_monitor_event import IMonitorEvent
    from .interface_main_keyboard_event import IMainKeyboardEvent


class IEvents(ABC):
    @abstractmethod
    def on(self, event: str, callback: Callable[[str], None]) -> None:
        """Connect to desktop environment events"""
        ...

    @property
    @abstractmethod
    def workspace(self) -> IWorkspaceEvent:
        """Return a desktop environment methods"""
        ...

    @property
    @abstractmethod
    def window(self) -> IWindowEvent:
        """Return a desktop environment methods"""
        ...

    @property
    @abstractmethod
    def monitor(self) -> IMonitorEvent:
        """Return a desktop environment methods"""
        ...

    @property
    @abstractmethod
    def main_keyboard(self) -> IMainKeyboardEvent:
        """Return a desktop environment methods"""
        ...
