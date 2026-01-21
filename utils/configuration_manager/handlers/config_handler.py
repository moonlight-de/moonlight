from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict


class BaseConfigHandler(ABC):
    def __init__(self, path: Path) -> None:
        self.path = path

    @abstractmethod
    def load(self) -> Dict[str, Any]:
        """
        Load and parse the config file. Must return a dict.
        Should NOT perform merging or validation.
        """
        ...
