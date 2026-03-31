from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any

from utils.jsonc_manager import JSONC
from utils.tools import MergeDicts

from .config_file_loader import ConfigFileLoader
from .config_import_resolver import ConfigImportResolver, ConfigImportError

from rich import print

from utils.exceptions import (
    JsoncParseError,
    ConfigValidationError,
)

if TYPE_CHECKING:
    from utils import ConfigManager


jsonc = JSONC()


class ConfigManagerLoader:
    def __init__(self, config_manager: "ConfigManager") -> None:
        self.config_manager = config_manager
        self.file_loader = ConfigFileLoader()
        self.import_resolver = ConfigImportResolver(
            loader=self.file_loader,
            merger=MergeDicts,
        )

    def load_default_config(self) -> dict[str, Any]:
        raw = self.file_loader.load(self.config_manager.default_config_file)
        resolved = self.import_resolver.resolve(
            raw,
            self.config_manager.default_config_file.parent,
        )
        return resolved if isinstance(resolved, dict) else {}

    def load_user_config(self) -> dict[str, Any]:
        raw = self.file_loader.load(self.config_manager.user_config_file)
        resolved = self.import_resolver.resolve(
            raw,
            self.config_manager.user_config_file.parent,
        )
        return resolved if isinstance(resolved, dict) else {}

    def load_backup_config(self) -> dict[str, Any]:
        raw = self.file_loader.load(self.config_manager.backup_config_file)
        resolved = self.import_resolver.resolve(
            raw,
            self.config_manager.backup_config_file.parent,
        )
        return resolved if isinstance(resolved, dict) else {}

    def save_backup_config(self, config: dict[str, Any]) -> None:
        jsonc.write(self.config_manager.backup_config_file, config)

    def load(self) -> dict[str, Any]:
        default_config: dict[str, Any] = {}

        try:
            default_config = self.load_default_config()
            self.config_manager._validator.validate(default_config)
        except (
            JsoncParseError,
            ConfigValidationError,
            ConfigImportError,
            ValueError,
        ) as default_error:
            print(
                default_error.pretty()  # type: ignore
                if hasattr(default_error, "pretty")
                else str(default_error),
                file=sys.stderr,
            )

            try:
                backup_config = self.load_backup_config()
                if isinstance(backup_config, dict) and backup_config:
                    self.config_manager._validator.validate(backup_config)
                    return backup_config
            except (
                JsoncParseError,
                ConfigValidationError,
                ConfigImportError,
                ValueError,
            ) as backup_error:
                print(
                    backup_error.pretty()  # type: ignore
                    if hasattr(backup_error, "pretty")
                    else str(backup_error),
                    file=sys.stderr,
                )

            raise RuntimeError("Default config and backup config are both invalid.")

        try:
            user_config = self.load_user_config()
            effective = self.config_manager._tools.merge_config(
                default_config,
                user_config,
            )

            self.config_manager._validator.validate(effective)
            self.save_backup_config(effective)
            return effective

        except (
            JsoncParseError,
            ConfigValidationError,
            ConfigImportError,
            ValueError,
        ) as user_error:
            print(
                user_error.pretty()  # type: ignore
                if hasattr(user_error, "pretty")
                else str(user_error),
                file=sys.stderr,
            )

        try:
            backup_config = self.load_backup_config()
            if isinstance(backup_config, dict) and backup_config:
                self.config_manager._validator.validate(backup_config)
                return backup_config

        except (
            JsoncParseError,
            ConfigValidationError,
            ConfigImportError,
            ValueError,
        ) as backup_error:
            print(
                backup_error.pretty()  # type: ignore
                if hasattr(backup_error, "pretty")
                else str(backup_error),
                file=sys.stderr,
            )

        return default_config
