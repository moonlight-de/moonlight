from __future__ import annotations

import json
from typing import Optional

from ignis.services.hyprland import (
    HyprlandMonitor,
    HyprlandService,
    HyprlandWindow,
    HyprlandWorkspace,
)

from .events import HyprEvents
from .main_keyboard import HyprMainKeyboard
from .monitors import HyprMonitors
from .windows import HyprWindows
from .workspace import HyprWorkspace
from services.wayland_ipc.interfaces import (
    IEvents,
    IMainKeyboard,
    IMonitors,
    IWaylandIpc,
    IWindows,
    IWorkspace,
)


class Hyprctl(IWaylandIpc):
    def __init__(self) -> None:
        self.hypr = HyprlandService.get_default()

        self._workspace: Optional[IWorkspace] = None
        self._windows: Optional[IWindows] = None
        self._monitors: Optional[IMonitors] = None
        self._main_keyboard: Optional[IMainKeyboard] = None
        self._events: Optional[HyprEvents] = None

    @property
    def workspace(self) -> IWorkspace:
        if self._workspace is None:
            self._workspace = HyprWorkspace(self)
        return self._workspace

    @property
    def windows(self) -> IWindows:
        if self._windows is None:
            self._windows = HyprWindows(self)
        return self._windows

    @property
    def monitors(self) -> IMonitors:
        if self._monitors is None:
            self._monitors = HyprMonitors(self)
        return self._monitors

    @property
    def main_keyboard(self) -> IMainKeyboard:
        if self._main_keyboard is None:
            self._main_keyboard = HyprMainKeyboard(self)
        return self._main_keyboard

    @property
    def events(self) -> IEvents:
        if self._events is None:
            self._events = HyprEvents(self)
        return self._events

    def switch_to_workspace(self, workspace_id: int) -> None:
        self.hypr.switch_to_workspace(workspace_id)

    def _refresh_workspaces(self) -> None:
        if not self.hypr.is_available:
            return

        data_list = json.loads(self.hypr.send_command("j/workspaces"))
        old_workspaces = dict(self.hypr._workspaces)
        new_workspaces: dict[int, HyprlandWorkspace] = {}

        for data in data_list:
            workspace_id = data["id"]
            workspace = old_workspaces.get(workspace_id)

            if workspace is None:
                workspace = HyprlandWorkspace(self.hypr)
                workspace.sync(data)
                self.hypr.emit("workspace-added", workspace)
            else:
                workspace.sync(data)

            new_workspaces[workspace_id] = workspace

        for workspace_id, workspace in old_workspaces.items():
            if workspace_id not in new_workspaces:
                workspace.emit("destroyed")

        self.hypr._workspaces = dict(sorted(new_workspaces.items()))
        self.hypr.notify("workspaces")
        self._sync_active_workspace()

    def _refresh_windows(self) -> None:
        if not self.hypr.is_available:
            return

        data_list = json.loads(self.hypr.send_command("j/clients"))
        old_windows = dict(self.hypr._windows)
        new_windows: dict[str, HyprlandWindow] = {}

        for data in data_list:
            address = data["address"]
            window = old_windows.get(address)

            if window is None:
                window = HyprlandWindow()
                window.sync(data)
                self.hypr.emit("window-added", window)
            else:
                window.sync(data)

            new_windows[address] = window

        for address, window in old_windows.items():
            if address not in new_windows:
                window.emit("closed")

        self.hypr._windows = dict(sorted(new_windows.items()))
        self.hypr.notify("windows")
        self._sync_active_window()

    def _refresh_monitors(self) -> None:
        if not self.hypr.is_available:
            return

        data_list = json.loads(self.hypr.send_command("j/monitors"))
        old_monitors = dict(self.hypr._monitors)
        new_monitors: dict[str, HyprlandMonitor] = {}

        for data in data_list:
            name = data["name"]
            monitor = old_monitors.get(name)

            if monitor is None:
                monitor = HyprlandMonitor()
                monitor.sync(data)
                self.hypr.emit("monitor-added", monitor)
            else:
                monitor.sync(data)

            new_monitors[name] = monitor

        for name, monitor in old_monitors.items():
            if name not in new_monitors:
                monitor.emit("removed")

        self.hypr._monitors = dict(sorted(new_monitors.items()))
        self.hypr.notify("monitors")
        self._sync_monitor_active_workspace()

    def _refresh_main_keyboard(self) -> None:
        if not self.hypr.is_available:
            return

        devices = json.loads(self.hypr.send_command("j/devices"))
        for keyboard_data in devices.get("keyboards", []):
            if keyboard_data.get("main") is True:
                self.hypr._main_keyboard.sync(keyboard_data)
                self.hypr.notify("main-keyboard")
                break

    def _sync_active_workspace(self) -> None:
        if not self.hypr.is_available:
            return

        workspace_data = json.loads(self.hypr.send_command("j/activeworkspace"))
        self.hypr._active_workspace.sync(workspace_data)
        self.hypr.notify("active-workspace")
        self._sync_monitor_active_workspace()

    def _sync_active_window(self) -> None:
        if not self.hypr.is_available:
            return

        active_window_data = json.loads(self.hypr.send_command("j/activewindow"))
        if active_window_data == {}:
            active_window_data = HyprlandWindow().data

        self.hypr._active_window.sync(active_window_data)
        self.hypr.notify("active-window")

    def _sync_monitor_active_workspace(self) -> None:
        active_workspace = self.hypr.active_workspace
        monitor_name = getattr(active_workspace, "monitor", "")
        if not monitor_name:
            return

        monitor = self.hypr.get_monitor_by_name(monitor_name)
        if monitor is None:
            return

        monitor.sync(
            {
                "activeWorkspace": {
                    "id": active_workspace.id,
                    "name": active_workspace.name,
                }
            }
        )
        self.hypr.notify("monitors")
