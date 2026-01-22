from services.wayland_ipc.hyprland.models import WindowsModel
from services.wayland_ipc.interfaces import IWindows
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.hypr import Hypr


class HyprWindows(IWindows):
    def __init__(self, hyprland_ipc: "Hypr") -> None:
        self.hyprland_ipc = hyprland_ipc

    def list_windows(self) -> list[WindowsModel]:
        windows = self.hyprland_ipc.hypr.windows
        windows_list: list[WindowsModel] = []

        for window in windows:
            windows_list.append(self._window_schema(window))

        return windows_list

    def _window_schema(self, window) -> WindowsModel:
        return WindowsModel(
            address=window.address,
            at=window.at,
            size=window.size,
            workspace_id=window.workspace_id,
            floating=window.floating,
            monitor=window.monitor,
            monitor_id=window.monitor_id,
            class_name=window.class_name,
            title=window.title,
            initial_title=window.initial_title,
            pid=window.pid,
            pinned=window.pinned,
            fullscreen=window.fullscreen,
        )

    def get_window_by_address(self, address: str) -> WindowsModel | None:
        for window in self.hyprland_ipc.hypr.windows:
            if window.address == address:
                return self._window_schema(window)

    def list_windows_on_workspace(self, workspace_id: int) -> List[WindowsModel]:
        windows = self.hyprland_ipc.hypr.windows
        windows_list: list[WindowsModel] = []

        for window in windows:
            if window.workspace_id == workspace_id:
                windows_list.append(self._window_schema(window))

        return windows_list
