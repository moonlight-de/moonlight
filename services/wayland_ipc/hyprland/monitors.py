from __future__ import annotations

from typing import TYPE_CHECKING

from services.wayland_ipc.hyprland.models import MonitorsModel
from services.wayland_ipc.interfaces import IMonitors

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprMonitors(IMonitors):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
    def list_monitors(self) -> list[MonitorsModel]:
        return [
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
            for monitor in self.hyprland_ipc.hypr.monitors
        ]

    def refresh(self) -> None:
        self.hyprland_ipc._refresh_monitors()
