from __future__ import annotations

import json
from services.wayland_ipc.hyprland.models import MainKeyboardModel
from services.wayland_ipc.interfaces import IMainKeyboard
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from services.wayland_ipc.hyprland import Hyprctl


class HyprMainKeyboard(IMainKeyboard):
    def __init__(self, hyprland_ipc: Hyprctl) -> None:
        self.hyprland_ipc = hyprland_ipc

    @property
    def keyboard(self) -> MainKeyboardModel:
        kb = self.hyprland_ipc.hypr.main_keyboard

        return MainKeyboardModel(
            address=kb.address,
            name=kb.name,
            rules=kb.rules,
            model=kb.model,
            layout=self._layout_handler(kb.layout),
            variant=kb.variant,
            options=kb.options,
            active_keymap=kb.active_keymap,
            caps_lock=kb.caps_lock,
            num_lock=kb.num_lock,
            main=kb.main,
        )

    def refresh(self) -> None:
        data_list = json.loads(self.hyprland_ipc.hypr.send_command("j/devices"))[
            "keyboards"
        ]

        for kb_data in data_list:
            if kb_data["main"] is True:
                self.hyprland_ipc.hypr._main_keyboard.sync(kb_data)

    def _layout_handler(self, layout: str) -> list[str]:
        parts = map(str.strip, layout.split(","))
        return [part for part in parts if part]
