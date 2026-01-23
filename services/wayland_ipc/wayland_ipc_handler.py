from loguru import logger
from utils.tools import DefineDesktop

from services.wayland_ipc.hyprland.hypr import Hyprctl

REGISTER_WAYLAND_IPC = [
    Hyprctl,
]


class WaylandIpcHandler:
    _instance = None

    @classmethod
    def ipc(cls):
        if cls._instance is not None:
            return cls._instance

        desktop_env = DefineDesktop.get()
        for wayland_ipc in REGISTER_WAYLAND_IPC:
            try:
                name = wayland_ipc.name()
            except TypeError:
                name = wayland_ipc().name()
            if desktop_env == name:
                cls._instance = wayland_ipc()
                return cls._instance

        logger.error(f"Wayland IPC not found for desktop environment: {desktop_env}")
        return None
