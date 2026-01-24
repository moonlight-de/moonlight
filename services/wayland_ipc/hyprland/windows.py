import json
from ignis.services.hyprland import HyprlandWindow
from services.wayland_ipc.hyprland.models import WindowsModel
from services.wayland_ipc.interfaces import IWindows
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprWindows(IWindows):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
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

    def list_windows_on_workspace(
        self, workspace_id: int
    ) -> Optional[List[WindowsModel]]:
        windows = self.hyprland_ipc.hypr.windows
        windows_list: list[WindowsModel] = []

        for window in windows:
            if window.workspace_id == workspace_id:
                windows_list.append(self._window_schema(window))

        return windows_list

    def refresh(self) -> None:
        data_list = json.loads(self.hyprland_ipc.hypr.send_command("j/clients"))

        old_windows = self.hyprland_ipc.hypr._windows
        new_windows: dict[str, HyprlandWindow] = {}

        for data in data_list:
            address = data["address"]

            if address in old_windows:
                win = old_windows[address]
            else:
                win = HyprlandWindow()
                self.hyprland_ipc.hypr.emit("window-added", win)

            win.sync(data)
            new_windows[address] = win

        for address, win in old_windows.items():
            if address not in new_windows:
                win.emit("closed")

        self.hyprland_ipc.hypr._windows = dict(sorted(new_windows.items()))
