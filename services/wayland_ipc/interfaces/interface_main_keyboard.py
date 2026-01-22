from abc import ABC, abstractmethod
from services.wayland_ipc.hyprland.models import MainKeyboardModel


class IMainKeyboard(ABC):
    """
    Interface for the main keyboard.
    """

    @abstractmethod
    def keyboard(self) -> MainKeyboardModel:
        """
        Return the main keyboard as a dictionary.

        Example:
             MainKeyboardModel(
                address="0x558c8deb0f40",
                name="Logitech K120",
                layout="us",
                variant="",
                options="",
                active_keymap="us",
                caps_lock=False,
                num_lock=False,
                main=True,
            )
        """
        ...
