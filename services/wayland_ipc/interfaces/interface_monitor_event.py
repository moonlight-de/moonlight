from abc import ABC, abstractmethod
from typing import Callable


class IMonitorEvent(ABC):
    @abstractmethod
    def moved(self, callback: Callable) -> None:
        """Monitor moved"""

    @abstractmethod
    def added(self, callback: Callable) -> None:
        """Monitor added"""

    @abstractmethod
    def removed(self, callback: Callable) -> None:
        """Monitor removed"""
