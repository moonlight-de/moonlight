from .interface_wayland_ipc import IWaylandIpc
from .interface_workspaces import IWorkspace
from .interface_windows import IWindows
from .interface_monitors import IMonitors
from .interface_main_keyboard import IMainKeyboard

from .interface_events import IEvents
from .interface_workspace_event import IWorkspaceEvent
from .interface_window_event import IWindowEvent
from .interface_monitor_event import IMonitorEvent
from .interface_main_keyboard_event import IMainKeyboardEvent

__all__ = [
    "IWaylandIpc",
    "IWorkspace",
    "IWindows",
    "IMonitors",
    "IMainKeyboard",
    "IEvents",
    "IWorkspaceEvent",
    "IWindowEvent",
    "IMonitorEvent",
    "IMainKeyboardEvent",
]
