from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Callable, Optional

from gi.repository import GLib  # type: ignore

from services.wayland_ipc.interfaces import (
    IEvents,
    IMainKeyboardEvent,
    IMonitorEvent,
    IWindowEvent,
    IWorkspaceEvent,
)

from .event_main_keyboard import MainKeyboardEvent
from .event_monitor import MonitorEvent
from .event_window import WindowEvent
from .event_workspace import WorkspaceEvent
from .hyprland_event import HyprlandEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl

log = logging.getLogger(__name__)


class HyprEvents(IEvents):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc
        self.hypr = hyprland_ipc.hypr

        self._callbacks: dict[str, list[Callable[[], None]]] = {}

        self._workspace: Optional[WorkspaceEvent] = None
        self._window: Optional[WindowEvent] = None
        self._main_keyboard: Optional[MainKeyboardEvent] = None
        self._monitor: Optional[MonitorEvent] = None

        self._workspace_snapshot = self._snapshot_workspaces()
        self._window_snapshot = self._snapshot_windows()
        self._monitor_snapshot = self._snapshot_monitors()
        self._keyboard_snapshot = self._snapshot_keyboard()

        self._active_workspace_id = getattr(self.hypr.active_workspace, "id", 0)
        self._active_workspace_monitor = getattr(
            self.hypr.active_workspace, "monitor", ""
        )
        self._active_window_address = getattr(self.hypr.active_window, "address", "")

        self._bind_service_signals()

    def on(self, event: HyprlandEvent, callback: Callable[[], None]) -> None:
        self._callbacks.setdefault(str(event).lower(), []).append(callback)

    @property
    def workspace(self) -> IWorkspaceEvent:
        if self._workspace is None:
            self._workspace = WorkspaceEvent(self)
        return self._workspace

    @property
    def window(self) -> IWindowEvent:
        if self._window is None:
            self._window = WindowEvent(self)
        return self._window

    @property
    def main_keyboard(self) -> IMainKeyboardEvent:
        if self._main_keyboard is None:
            self._main_keyboard = MainKeyboardEvent(self)
        return self._main_keyboard

    @property
    def monitor(self) -> IMonitorEvent:
        if self._monitor is None:
            self._monitor = MonitorEvent(self)
        return self._monitor

    def _bind_service_signals(self) -> None:
        self.hypr.connect(
            "notify::workspaces",
            lambda *_: GLib.idle_add(self._handle_workspaces_notify),
        )
        self.hypr.connect(
            "notify::active-workspace",
            lambda *_: GLib.idle_add(self._handle_active_workspace_notify),
        )
        self.hypr.connect(
            "notify::windows",
            lambda *_: GLib.idle_add(self._handle_windows_notify),
        )
        self.hypr.connect(
            "notify::active-window",
            lambda *_: GLib.idle_add(self._handle_active_window_notify),
        )
        self.hypr.connect(
            "notify::monitors",
            lambda *_: GLib.idle_add(self._handle_monitors_notify),
        )
        self.hypr.connect(
            "notify::main-keyboard",
            lambda *_: GLib.idle_add(self._handle_main_keyboard_notify),
        )

        self.hypr.connect(
            "workspace-added",
            lambda *_: GLib.idle_add(self._emit, HyprlandEvent.CREATE_WORKSPACE_V2),
        )
        self.hypr.connect(
            "window-added",
            lambda *_: GLib.idle_add(self._emit, HyprlandEvent.OPEN_WINDOW),
        )
        self.hypr.connect(
            "monitor-added",
            lambda *_: GLib.idle_add(self._emit_monitor_added_pair),
        )

    def _emit_monitor_added_pair(self) -> bool:
        self._emit(HyprlandEvent.MONITOR_ADDED)
        self._emit(HyprlandEvent.MONITOR_ADDED_V2)
        return False

    def _emit(self, event: HyprlandEvent | str) -> bool:
        key = str(event).lower()
        for callback in list(self._callbacks.get(key, [])):
            try:
                callback()
            except Exception:
                log.exception("Error in Hyprland callback for event %s", key)
        return False

    def _snapshot_workspaces(self) -> dict[int, tuple[str, str, int, int, bool]]:
        return {
            ws.id: (
                ws.name,
                ws.monitor,
                ws.monitor_id,
                ws.windows,
                ws.has_fullscreen,
            )
            for ws in self.hypr.workspaces
        }

    def _snapshot_windows(
        self,
    ) -> dict[str, tuple[int, bool, bool, int, str, str, bool]]:
        return {
            window.address: (
                window.workspace_id,
                window.floating,
                window.fullscreen,
                window.monitor,
                window.class_name,
                window.title,
                window.pinned,
            )
            for window in self.hypr.windows
        }

    def _snapshot_monitors(
        self,
    ) -> dict[str, tuple[int, int, int, float, bool, str | None, str | None]]:
        return {
            monitor.name: (
                monitor.id,
                monitor.width,
                monitor.height,
                monitor.scale,
                monitor.focused,
                monitor.description,
                monitor.serial,
            )
            for monitor in self.hypr.monitors
        }

    def _snapshot_keyboard(self) -> tuple[str, bool, bool]:
        keyboard = self.hypr.main_keyboard
        return (
            keyboard.active_keymap,
            keyboard.caps_lock,
            keyboard.num_lock,
        )

    def _handle_active_workspace_notify(self) -> bool:
        new_id = getattr(self.hypr.active_workspace, "id", 0)
        new_monitor = getattr(self.hypr.active_workspace, "monitor", "")

        workspace_changed = (
            new_id != self._active_workspace_id
            or new_monitor != self._active_workspace_monitor
        )
        monitor_changed = new_monitor != self._active_workspace_monitor

        self._active_workspace_id = new_id
        self._active_workspace_monitor = new_monitor

        if workspace_changed:
            self._emit(HyprlandEvent.WORKSPACE)
            self._emit(HyprlandEvent.WORKSPACE_V2)

        if monitor_changed:
            self._emit(HyprlandEvent.FOCUSED_MON)
            self._emit(HyprlandEvent.FOCUSED_MON_V2)

        return False

    def _handle_workspaces_notify(self) -> bool:
        old_snapshot = self._workspace_snapshot
        new_snapshot = self._snapshot_workspaces()

        old_ids = set(old_snapshot)
        new_ids = set(new_snapshot)

        if old_ids - new_ids:
            self._emit(HyprlandEvent.DESTROY_WORKSPACE_V2)

        for workspace_id in old_ids & new_ids:
            old_name, old_monitor, old_monitor_id, *_ = old_snapshot[workspace_id]
            new_name, new_monitor, new_monitor_id, *_ = new_snapshot[workspace_id]

            if old_name != new_name:
                self._emit(HyprlandEvent.RENAME_WORKSPACE)

            if (old_monitor, old_monitor_id) != (new_monitor, new_monitor_id):
                self._emit(HyprlandEvent.MOVE_WORKSPACE_V2)

        self._workspace_snapshot = new_snapshot
        return False

    def _handle_windows_notify(self) -> bool:
        old_snapshot = self._window_snapshot
        new_snapshot = self._snapshot_windows()

        old_addresses = set(old_snapshot)
        new_addresses = set(new_snapshot)

        if old_addresses - new_addresses:
            self._emit(HyprlandEvent.CLOSE_WINDOW)

        for address in old_addresses & new_addresses:
            old_workspace_id, old_floating, old_fullscreen, *_ = old_snapshot[address]
            new_workspace_id, new_floating, new_fullscreen, *_ = new_snapshot[address]

            if old_workspace_id != new_workspace_id:
                self._emit(HyprlandEvent.MOVE_WINDOW_V2)

            if old_floating != new_floating:
                self._emit(HyprlandEvent.CHANGE_FLOATING_MODE)

            if old_fullscreen != new_fullscreen:
                self._emit(HyprlandEvent.FULLSCREEN)

        self._window_snapshot = new_snapshot
        return False

    def _handle_active_window_notify(self) -> bool:
        new_address = getattr(self.hypr.active_window, "address", "")
        if new_address != self._active_window_address:
            self._active_window_address = new_address
            self._emit(HyprlandEvent.ACTIVE_WINDOW)
        return False

    def _handle_monitors_notify(self) -> bool:
        old_snapshot = self._monitor_snapshot
        new_snapshot = self._snapshot_monitors()

        old_names = set(old_snapshot)
        new_names = set(new_snapshot)

        if new_names - old_names:
            self._emit(HyprlandEvent.MONITOR_ADDED)
            self._emit(HyprlandEvent.MONITOR_ADDED_V2)

        if old_names - new_names:
            self._emit(HyprlandEvent.MONITOR_REMOVED)
            self._emit(HyprlandEvent.MONITOR_REMOVED_V2)

        if old_names == new_names and old_snapshot != new_snapshot:
            self._emit(HyprlandEvent.MONITORS_CHANGED)

        self._monitor_snapshot = new_snapshot
        return False

    def _handle_main_keyboard_notify(self) -> bool:
        old_snapshot = self._keyboard_snapshot
        new_snapshot = self._snapshot_keyboard()

        if old_snapshot[0] != new_snapshot[0]:
            self._emit(HyprlandEvent.ACTIVE_LAYOUT)

        self._keyboard_snapshot = new_snapshot
        return False
