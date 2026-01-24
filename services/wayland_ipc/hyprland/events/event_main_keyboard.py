from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from ignis.utils import Poll
from gi.repository.GLib import idle_add  # type: ignore

from services.wayland_ipc.interfaces import IMainKeyboardEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.events import HyprEvents


class MainKeyboardEvent(IMainKeyboardEvent):
    def __init__(self, hypr_events: HyprEvents) -> None:
        self.hypr_events = hypr_events
        self.keyboard = hypr_events.hyprland_ipc.main_keyboard

        self._language = self.keyboard.keyboard.active_keymap
        self._capslock = self.keyboard.keyboard.caps_lock
        self._numlock = self.keyboard.keyboard.num_lock

        self._caps_cb: Optional[Callable] = None
        self._num_cb: Optional[Callable] = None

        Poll(
            timeout=300,
            callback=lambda _: self._poll_keyboard(),
        )

    def language_changed(self, callback: Callable) -> None:
        def handler():
            new_lang = self.keyboard.keyboard.active_keymap
            if new_lang != self._language:
                self._language = new_lang
                idle_add(callback)

        self.hypr_events.on("activelayout", handler)

    def capslock_changed(self, callback: Callable) -> None:
        self._caps_cb = callback

    def numlock_changed(self, callback: Callable) -> None:
        self._num_cb = callback

    def _poll_keyboard(self):
        self.keyboard.refresh()
        kb = self.keyboard.keyboard

        if kb.caps_lock != self._capslock:
            self._capslock = kb.caps_lock
            if self._caps_cb:
                idle_add(self._caps_cb)

        if kb.num_lock != self._numlock:
            self._numlock = kb.num_lock
            if self._num_cb:
                idle_add(self._num_cb)

        return True
