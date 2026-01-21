from pathlib import Path
from typing import Any

from loguru import logger

from ..core.yaml_config import ConfigHandlerYaml
from ..core.jsonc_handler import ConfigHandlerJSONC
from ..core.config_handler import ConfigHandler


class ConfigLoader:
    YAML_EXT = {"yaml", "yml"}
    JSONC_EXT = "jsonc"

    @staticmethod
    def load(path: Path) -> Any:
        ext = path.suffix.lstrip(".").lower()
        if ext in ConfigLoader.YAML_EXT:
            handler: ConfigHandler = ConfigHandlerYaml(path)
        elif ext == ConfigLoader.JSONC_EXT:
            handler = ConfigHandlerJSONC(path)
        else:
            raise ValueError(f"Unsupported config extension: {ext} ({path})")

        logger.info(f"Loading config from {path}")
        return handler.load()
