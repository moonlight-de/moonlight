from abc import ABC, abstractmethod
from typing import Callable


class IWorkspaceEvent(ABC):
    @abstractmethod
    def changed(self, callback: Callable) -> None:
        """Active workspace changed"""

    @abstractmethod
    def created(self, callback: Callable) -> None:
        """Workspace created"""

    @abstractmethod
    def destroyed(self, callback: Callable) -> None:
        """Workspace destroyed"""

    @abstractmethod
    def moved(self, callback: Callable) -> None:
        """Workspace moved"""

    @abstractmethod
    def renamed(self, callback: Callable) -> None:
        """Workspace renamed"""
