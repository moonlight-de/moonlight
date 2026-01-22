from abc import ABC, abstractmethod
from typing import List
from services.wayland_ipc.hyprland.models import MonitorsModel


class IMonitors(ABC):
    """
    Interface for interacting with monitors.
    """

    @abstractmethod
    def list_monitors(self) -> List[MonitorsModel]:
        """
        Return a list of monitors as MonitorsModel instances.

        Example:
            [
                MonitorsModel(
                    id=0,
                    name="eDP-1",
                    description=None,
                    model=None,
                    serial=None,
                    width=1920,
                    height=1080,
                    physical_width=340,
                    physical_height=190,
                    refresh_rate=144.0,
                    scale=1.0,
                    focused=True,
                    available_modes=["1920x1080@144.00Hz","1920x1080@60.00Hz"],
                ),
                ...
            ]
        """
        ...
