from abc import ABC, abstractmethod
from typing import Callable


class IMainKeyboardEvent(ABC):
    @abstractmethod
    def language_changed(self, callback: Callable) -> None:
        """Language changed"""

    @abstractmethod
    def capslock_changed(self, callback: Callable) -> None:
        """Capslock changed"""

    @abstractmethod
    def numlock_changed(self, callback: Callable) -> None:
        """Numlock changed"""
