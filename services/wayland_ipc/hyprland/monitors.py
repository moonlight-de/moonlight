from services.wayland_ipc.hyprland.models import MonitorsModel
from services.wayland_ipc.interfaces import IMonitors
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.hypr import Hyprctl


class HyprMonitors(IMonitors):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

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
                    physical_width=monitor.physical_width,
                    physical_height=monitor.physical_height,
                    refresh_rate=monitor.refresh_rate,
                    scale=monitor.scale,
                    focused=monitor.focused,
                    available_modes=monitor.available_modes,
                )
            )

        return monitors_list
