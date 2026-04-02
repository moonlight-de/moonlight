from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from .interface_workspace_event import IWorkspaceEvent
    from .interface_window_event import IWindowEvent
    from .interface_monitor_event import IMonitorEvent
    from .interface_main_keyboard_event import IMainKeyboardEvent
    from services.wayland_ipc.hyprland.events.hyprland_event import HyprlandEvent


class IEvents(ABC):
    @abstractmethod
    def on(self, event: "HyprlandEvent", callback: Callable[[], None]) -> None:
        """Connect to desktop environment events."""
        ...

    @property
    @abstractmethod
    def workspace(self) -> IWorkspaceEvent:
        """Workspace event facade."""
        ...

    @property
    @abstractmethod
    def window(self) -> IWindowEvent:
        """Window event facade."""
        ...

    @property
    @abstractmethod
    def monitor(self) -> IMonitorEvent:
        """Monitor event facade."""
        ...

    @property
    @abstractmethod
    def main_keyboard(self) -> IMainKeyboardEvent:
        """Keyboard event facade."""
        ...
