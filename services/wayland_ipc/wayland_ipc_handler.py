from typing import Type
from utils.tools import DefineDesktop
from loguru import logger
from utils.constants.supported_desktops import SupportedDesktops as sd

from services.wayland_ipc.hyprland.hyprctl import Hyprctl
from services.wayland_ipc.interfaces import IWaylandIpc

WAYLAND_IPC_REGISTRY: dict[str, Type[IWaylandIpc]] = {
    sd.HYPRLAND: Hyprctl,
}


class WaylandIpcHandler:
    """
    Wayland IPC Handler
    """

    @staticmethod
    def create_wayland_ipc() -> IWaylandIpc:
        desktop = DefineDesktop.get()
        cls = WAYLAND_IPC_REGISTRY[desktop]
        if not cls:
            logger.error(f"Wayland IPC not found for desktop environment: {desktop}")
            raise RuntimeError(f"No Wayland IPC for {desktop}")
        return cls()
