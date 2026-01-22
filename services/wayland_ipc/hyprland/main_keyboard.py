from services.wayland_ipc.hyprland.models import MainKeyboardModel
from services.wayland_ipc.interfaces import IMainKeyboard
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.hypr import Hypr


class HyprMainKeyboard(IMainKeyboard):
    def __init__(self, hyprland_ipc: "Hypr") -> None:
        self.hyprland_ipc = hyprland_ipc

    def keyboard(self) -> MainKeyboardModel:
        kb = self.hyprland_ipc.hypr.main_keyboard

        return MainKeyboardModel(
            address=kb.address,
            name=kb.name,
            rules=kb.rules,
            model=kb.model,
            layout=kb.layout,
            variant=kb.variant,
            options=kb.options,
            active_keymap=kb.active_keymap,
            caps_lock=kb.caps_lock,
            num_lock=kb.num_lock,
            main=kb.main,
        )
