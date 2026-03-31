from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Any

from utils.tools import MergeDicts
from utils.jsonc_manager import JSONC

jsonc = JSONC()

if TYPE_CHECKING:
    from ..config_manager import ConfigManager


class ConfigManagerTools:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager

    def read_default_config(self) -> dict[str, Any]:
        return jsonc.read(self.config_manager.default_config_file)

    def read_user_config(self) -> dict[str, Any]:
        return jsonc.read(self.config_manager.user_config_file)

    def read_backup_config(self) -> dict[str, Any]:
        return jsonc.read(self.config_manager.backup_config_file)

    def merge_config(
        self,
        default_config: dict[str, Any],
        user_config: dict[str, Any],
    ) -> dict[str, Any]:
        return MergeDicts.merge(
            base=deepcopy(default_config),
            override=user_config,
        )

    def get_by_path(
        self,
        data: dict[str, Any],
        path: str,
        default: Any = None,
    ) -> Any:
        current: Any = data

        if not path:
            return current

        for part in path.split("."):
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]

        return current

    def has_path(self, data: dict[str, Any], path: str) -> bool:
        sentinel = object()
        return self.get_by_path(data, path, sentinel) is not sentinel
