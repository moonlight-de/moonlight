from __future__ import annotations

from pathlib import Path

from gi.repository import GObject  # type: ignore
from ignis.gobject import IgnisGObject


class HyprlandIPCListener(IgnisGObject):
    """
    Compatibility shim.

    The current Hyprland event facade no longer opens its own socket listener and
    now relies on Ignis `HyprlandService` as the single source of truth.
    This class is intentionally kept as a no-op to avoid import errors in older code.
    """

    __gsignals__ = {
        "raw-event": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, str),
        ),
    }

    def __init__(self, socket_path: Path) -> None:
        super().__init__()
        self.socket_path = socket_path

    def start(self) -> None:
        return None
