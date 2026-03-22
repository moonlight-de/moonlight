from os import getenv
from .paths import XDG_RUNTIME_DIR
from pathlib import Path


class SupportedDesktops:
    """
    List of supported desktops
    """

    HYPRLAND = "hyprland"
    HYPRLAND_INSTANCE_SIGNATURE = Path(
        getenv("HYPRLAND_INSTANCE_SIGNATURE", "/run/user/1000")
    )
    HYPR_SOCKET_DIR = XDG_RUNTIME_DIR / "hypr" / HYPRLAND_INSTANCE_SIGNATURE

    SWAY = "sway"
    NIRI = "niri"

    DESKTOPS_LIST = [
        HYPRLAND,
        SWAY,
        NIRI,
    ]
