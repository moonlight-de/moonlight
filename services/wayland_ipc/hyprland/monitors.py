import json
from services.wayland_ipc.hyprland.models import MonitorsModel
from services.wayland_ipc.interfaces import IMonitors
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprMonitors(IMonitors):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
    def list_monitors(self) -> list[MonitorsModel]:
        monitors = self.hyprland_ipc.hypr.monitors
        monitors_list: list[MonitorsModel] = []

        for monitor in monitors:
            monitors_list.append(
                MonitorsModel(
                    id=monitor.id,
                    name=monitor.name,
                    description=monitor.description,
                    model=monitor.model,
                    serial=monitor.serial,
                    width=monitor.width,
                    height=monitor.height,
                    refresh_rate=monitor.refresh_rate,
                    scale=monitor.scale,
                    focused=monitor.focused,
                    available_modes=monitor.available_modes,
                )
            )

        return monitors_list

    def refresh(self) -> None:
        """
        Refresh the list of monitors.
        """
        data_list = json.loads(self.hyprland_ipc.hypr.send_command("j/monitors"))

        old_monitors = self.hyprland_ipc.hypr._monitors
        new_monitors: dict[str, object] = {}

        for data in data_list:
            name = data["name"]

            if name in old_monitors:
                monitor = old_monitors[name]
            else:
                monitor = self.hyprland_ipc.hypr._OBJ_TYPES["monitor"].cr_func()
                self.hyprland_ipc.hypr.emit("monitor-added", monitor)

            monitor.sync(data)
            new_monitors[name] = monitor

        for name, monitor in old_monitors.items():
            if name not in new_monitors:
                monitor.emit("removed")

        self.hyprland_ipc.hypr._monitors = dict(sorted(new_monitors.items()))  # type: ignore
