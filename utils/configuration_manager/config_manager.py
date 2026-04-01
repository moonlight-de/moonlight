from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.constants import (
    PathHandler,
    CONFIG_SCHEMA,
    DEFAULT_CONFIG_FILE,
    APP_CONFIG_DIR,
    CONFIG_FILE_NAME,
)
from utils.exceptions import ConfigKeyNotFoundError

from .internals import ConfigManagerTools
from .internals import ConfigManagerLoader
from .internals.config_validator import ConfigValidator
from .internals.config_accessor import ConfigNode


class ConfigManager:
    def __init__(self) -> None:
        PathHandler(APP_CONFIG_DIR, folder=True)

        self.default_config_file = DEFAULT_CONFIG_FILE
        self.schema_file = CONFIG_SCHEMA
        self.user_config_file = APP_CONFIG_DIR / CONFIG_FILE_NAME
        self.backup_config_file = APP_CONFIG_DIR / "config.backup.jsonc"

        self._tools = ConfigManagerTools(self)
        self._validator = ConfigValidator(self.schema_file)
        self._loader = ConfigManagerLoader(self)

        self._config_cache: dict[str, Any] | None = None
        self._tracked_config_files: set[Path] = {
            self.default_config_file.expanduser().resolve(strict=False),
            self.user_config_file.expanduser().resolve(strict=False),
            self.backup_config_file.expanduser().resolve(strict=False),
        }

        self.cfg = ConfigNode(self)

    def load(self) -> dict[str, Any]:
        self._config_cache = self._loader.load()
        return self._config_cache

    def load_for_runtime_reload(self) -> dict[str, Any]:
        self._config_cache = self._loader.load_for_runtime_reload()
        return self._config_cache

    def get_config(self, reload: bool = False) -> dict[str, Any]:
        if reload or self._config_cache is None:
            return self.load()
        return self._config_cache

    def set_tracked_config_files(self, paths: set[Path]) -> None:
        normalized = {path.expanduser().resolve(strict=False) for path in paths}
        self._tracked_config_files = normalized

    def get_tracked_config_files(self) -> set[Path]:
        return set(self._tracked_config_files)

    def get(self, path: str, default: Any = None, reload: bool = False) -> Any:
        active_config = self.get_config(reload=reload)

        sentinel = object()
        value = self._tools.get_by_path(active_config, path, sentinel)
        if value is not sentinel:
            return value

        backup_config = self._loader.load_backup_config()
        value = self._tools.get_by_path(backup_config, path, sentinel)
        if value is not sentinel:
            return value

        default_config = self._loader.load_default_config()
        value = self._tools.get_by_path(default_config, path, sentinel)
        if value is not sentinel:
            return value

        return default

    def require(self, path: str, reload: bool = False) -> Any:
        sentinel = object()
        value = self.get(path, default=sentinel, reload=reload)
        if value is sentinel:
            raise ConfigKeyNotFoundError(path)
        return value

    def has(self, path: str, reload: bool = False) -> bool:
        sentinel = object()
        return self.get(path, default=sentinel, reload=reload) is not sentinel
