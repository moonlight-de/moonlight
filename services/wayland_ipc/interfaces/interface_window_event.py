from abc import ABC, abstractmethod
from typing import Callable, Any


class IWindowEvent(ABC):
    @abstractmethod
    def focus_changed(self, callback: Callable) -> None:
        """Window became active"""

    @abstractmethod
    def opened(self, callback: Callable) -> None:
        """Window opened"""

    @abstractmethod
    def closed(self, callback: Callable) -> None:
        """Window closed"""

    @abstractmethod
    def moved(self, callback: Callable) -> None:
        """Window moved"""

    @abstractmethod
    def floating_changed(self, callback: Callable) -> None:
        """Window floating mode changed"""

    @abstractmethod
    def fullscreen_changed(self, callback: Callable) -> None:
        """Window fullscreen mode changed"""
