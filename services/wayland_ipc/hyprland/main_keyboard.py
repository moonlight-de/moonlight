from __future__ import annotations

from typing import TYPE_CHECKING

from services.wayland_ipc.hyprland.models import MainKeyboardModel
from services.wayland_ipc.interfaces import IMainKeyboard

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprMainKeyboard(IMainKeyboard):
    def __init__(self, hyprland_ipc: "Hyprctl") -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
    def keyboard(self) -> MainKeyboardModel:
        keyboard = self.hyprland_ipc.hypr.main_keyboard
        return MainKeyboardModel(
            address=keyboard.address,
            name=keyboard.name,
            rules=keyboard.rules,
            model=keyboard.model,
            layout=self._layout_handler(keyboard.layout),
            variant=keyboard.variant,
            options=keyboard.options,
            active_keymap=keyboard.active_keymap,
            caps_lock=keyboard.caps_lock,
            num_lock=keyboard.num_lock,
            main=keyboard.main,
        )

    def refresh(self) -> None:
        self.hyprland_ipc._refresh_main_keyboard()

    def _layout_handler(self, layout: str) -> list[str]:
        return [part for part in map(str.strip, layout.split(",")) if part]
