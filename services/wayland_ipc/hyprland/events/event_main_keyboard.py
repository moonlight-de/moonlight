from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Optional

from gi.repository.GLib import idle_add  # type: ignore
from ignis.utils import Poll

from services.wayland_ipc.interfaces import IMainKeyboardEvent

from .hyprland_event import HyprlandEvent

if TYPE_CHECKING:
    from services.wayland_ipc.hyprland.events import HyprEvents


class MainKeyboardEvent(IMainKeyboardEvent):
    def __init__(self, hypr_events: "HyprEvents") -> None:
        self.hypr_events = hypr_events
        self._main_keyboard = hypr_events.hyprland_ipc.main_keyboard

        keyboard = self._main_keyboard.keyboard
        self._language = keyboard.active_keymap
        self._capslock = keyboard.caps_lock
        self._numlock = keyboard.num_lock

        self._caps_cb: Optional[Callable[[], None]] = None
        self._num_cb: Optional[Callable[[], None]] = None

        self._poll = Poll(
            timeout=300,
            callback=lambda *_: self._poll_keyboard(),
        )

    def language_changed(self, callback: Callable) -> None:
        def handler() -> None:
            new_language = self._main_keyboard.keyboard.active_keymap
            if new_language != self._language:
                self._language = new_language
                callback()

        self.hypr_events.on(HyprlandEvent.ACTIVE_LAYOUT, handler)

    def capslock_changed(self, callback: Callable) -> None:
        self._caps_cb = callback

    def numlock_changed(self, callback: Callable) -> None:
        self._num_cb = callback

    def _poll_keyboard(self) -> bool:
        self._main_keyboard.refresh()
        keyboard = self._main_keyboard.keyboard

        if keyboard.caps_lock != self._capslock:
            self._capslock = keyboard.caps_lock
            if self._caps_cb is not None:
                idle_add(self._caps_cb)

        if keyboard.num_lock != self._numlock:
            self._numlock = keyboard.num_lock
            if self._num_cb is not None:
                idle_add(self._num_cb)

        return True
