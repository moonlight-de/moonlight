from pathlib import Path
from typing import Optional
from loguru import logger


class ConfigFinder:
    YAML_EXT = {"yaml", "yml"}
    JSONC_EXT = "jsonc"
    FILE_NAME = "config"

    def __init__(self, config_dir: Path):
        self.config_dir = config_dir

    def find(self) -> Optional[Path]:
        """
        Find config.yaml/yml first, then config.jsonc
        """
        for ext in self.YAML_EXT:
            candidate = self.config_dir / f"{self.FILE_NAME}.{ext}"
            if candidate.exists():
                return candidate

        candidate = self.config_dir / f"{self.FILE_NAME}.{self.JSONC_EXT}"
        if candidate.exists():
            return candidate

        return None
