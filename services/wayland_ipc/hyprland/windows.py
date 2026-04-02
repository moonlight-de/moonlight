from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from services.wayland_ipc.hyprland.models import WindowsModel
from services.wayland_ipc.interfaces import IWindows

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprWindows(IWindows):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
    def list_windows(self) -> list[WindowsModel]:
        return [
            self._window_schema(window) for window in self.hyprland_ipc.hypr.windows
        ]

    def _window_schema(self, window) -> WindowsModel:
        return WindowsModel(
            address=window.address,
            at=window.at,
            size=window.size,
            workspace_id=window.workspace_id,
            floating=window.floating,
            monitor_id=window.monitor,
            class_name=window.class_name,
            title=window.title,
            initial_title=window.initial_title,
            pid=window.pid,
            pinned=window.pinned,
            fullscreen=window.fullscreen,
        )

    def get_window_by_address(self, address: str) -> Optional[WindowsModel]:
        for window in self.hyprland_ipc.hypr.windows:
            if window.address == address:
                return self._window_schema(window)
        return None

    def list_windows_on_workspace(
        self,
        workspace_id: int,
    ) -> Optional[List[WindowsModel]]:
        windows = [
            self._window_schema(window)
            for window in self.hyprland_ipc.hypr.windows
            if window.workspace_id == workspace_id
        ]
        return windows

    def refresh(self) -> None:
        self.hyprland_ipc._refresh_windows()
