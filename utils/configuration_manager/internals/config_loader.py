from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

from rich import print
from utils.exceptions import (
    JsoncParseError,
    ConfigValidationError,
)
from utils.jsonc_manager import JSONC
from utils.tools import MergeDicts

from .config_file_loader import ConfigFileLoader
from .config_import_resolver import ConfigImportResolver, ConfigImportError

if TYPE_CHECKING:
    from utils import ConfigManager


jsonc = JSONC()

LOAD_ERRORS = (
    JsoncParseError,
    ConfigValidationError,
    ConfigImportError,
    ValueError,
)


class ConfigManagerLoader:
    def __init__(self, config_manager: ConfigManager) -> None:
        self.config_manager = config_manager
        self.file_loader = ConfigFileLoader()
        self.import_resolver = ConfigImportResolver(
            loader=self.file_loader,
            merger=MergeDicts,
        )

    def _print_error(self, error: Exception) -> None:
        print(
            error.pretty() if hasattr(error, "pretty") else str(error),  # type: ignore[attr-defined]
            file=sys.stderr,
        )

    def _load_resolved_file(self, path: Path) -> tuple[dict[str, Any], set[Path]]:
        raw = self.file_loader.load(path)
        resolved = self.import_resolver.resolve(raw, path.parent)

        tracked_paths: set[Path] = {path.expanduser().resolve(strict=False)}
        tracked_paths |= {
            imported_path.expanduser().resolve(strict=False)
            for imported_path in self.import_resolver.resolved_paths
        }

        if not isinstance(resolved, dict):
            return {}, tracked_paths

        return resolved, tracked_paths

    def _remember_tracked_config_files(self, *groups: set[Path]) -> None:
        tracked: set[Path] = set()

        for group in groups:
            tracked |= {path.expanduser().resolve(strict=False) for path in group}

        tracked.add(
            self.config_manager.user_config_file.expanduser().resolve(strict=False)
        )
        tracked.add(
            self.config_manager.default_config_file.expanduser().resolve(strict=False)
        )
        tracked.add(
            self.config_manager.backup_config_file.expanduser().resolve(strict=False)
        )

        self.config_manager.set_tracked_config_files(tracked)

    def load_default_config_with_paths(self) -> tuple[dict[str, Any], set[Path]]:
        return self._load_resolved_file(self.config_manager.default_config_file)

    def load_user_config_with_paths(self) -> tuple[dict[str, Any], set[Path]]:
        return self._load_resolved_file(self.config_manager.user_config_file)

    def load_backup_config_with_paths(self) -> tuple[dict[str, Any], set[Path]]:
        return self._load_resolved_file(self.config_manager.backup_config_file)

    def load_default_config(self) -> dict[str, Any]:
        return self.load_default_config_with_paths()[0]

    def load_user_config(self) -> dict[str, Any]:
        return self.load_user_config_with_paths()[0]

    def load_backup_config(self) -> dict[str, Any]:
        return self.load_backup_config_with_paths()[0]

    def save_backup_config(self, config: dict[str, Any]) -> None:
        jsonc.write(self.config_manager.backup_config_file, config)

    def load(self) -> dict[str, Any]:
        user_root = {self.config_manager.user_config_file}
        backup_root = {self.config_manager.backup_config_file}

        try:
            default_config, default_paths = self.load_default_config_with_paths()
            self.config_manager._validator.validate(default_config)
        except LOAD_ERRORS as default_error:
            self._print_error(default_error)

            try:
                backup_config, backup_paths = self.load_backup_config_with_paths()
                if isinstance(backup_config, dict) and backup_config:
                    self.config_manager._validator.validate(backup_config)
                    self._remember_tracked_config_files(backup_paths, user_root)
                    return backup_config
            except LOAD_ERRORS as backup_error:
                self._print_error(backup_error)

            raise RuntimeError("Default config and backup config are both invalid.")

        try:
            user_config, user_paths = self.load_user_config_with_paths()
            effective = self.config_manager._tools.merge_config(
                default_config,
                user_config,
            )

            self.config_manager._validator.validate(effective)
            self.save_backup_config(effective)
            self._remember_tracked_config_files(default_paths, user_paths, backup_root)
            return effective

        except LOAD_ERRORS as user_error:
            self._print_error(user_error)

        try:
            backup_config, backup_paths = self.load_backup_config_with_paths()
            if isinstance(backup_config, dict) and backup_config:
                self.config_manager._validator.validate(backup_config)
                self._remember_tracked_config_files(
                    default_paths,
                    backup_paths,
                    user_root,
                )
                return backup_config

        except LOAD_ERRORS as backup_error:
            self._print_error(backup_error)

        self._remember_tracked_config_files(default_paths, user_root, backup_root)
        return default_config

    def load_for_runtime_reload(self) -> dict[str, Any]:
        """
        Runtime-safe reload:
        - default must be valid
        - user config must be valid after merge
        - no fallback to backup here
        If runtime reload fails, caller should keep current UI as is.
        """
        default_config, default_paths = self.load_default_config_with_paths()
        self.config_manager._validator.validate(default_config)

        user_config, user_paths = self.load_user_config_with_paths()
        effective = self.config_manager._tools.merge_config(
            default_config,
            user_config,
        )
        self.config_manager._validator.validate(effective)

        self._remember_tracked_config_files(
            default_paths,
            user_paths,
            {self.config_manager.backup_config_file},
        )
        return effective
