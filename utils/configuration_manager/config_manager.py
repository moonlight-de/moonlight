from pathlib import Path
from typing import Dict, Any, List
import shutil

from utils import (
    MergeDicts,
    PathHandler,
    CONFIG_DEFAULT_NAMES,
    CONFIG_DEFAULT_SCHEMAS,
)

from .manager_handler.config_finder import ConfigFinder
from .manager_handler.config_loader import ConfigLoader
from .manager_handler.config_importer import ConfigImporter
from .manager_handler.schema_finder import SchemaFinder
from .manager_handler.schema_validator import SchemaValidator


class ConfigManager:
    """
    High-level manager:
      - manages default (root) config dir and user dir
      - requires a schemas_dir (optional; defaults to default_config_dir / 'schemas')
      - validates configs with schema(s)
      - seeds user dir from defaults if needed
      - returns merged dict default <- user
    """

    DEFAULT_NAMES = CONFIG_DEFAULT_NAMES
    DEFAULT_SCHEMAS = CONFIG_DEFAULT_SCHEMAS

    def __init__(
        self,
        user_dir: Path,
        default_config_dir: Path,
        schemas_dir: Path,
    ):
        self.user_dir = Path(user_dir)
        self.default_config_dir = Path(default_config_dir)
        PathHandler(self.default_config_dir, folder=True)

        self.schemas_dir = Path(schemas_dir)
        PathHandler(self.schemas_dir, folder=True)

    def _find_default_files(self) -> List[Path]:
        found: List[Path] = []
        for name in self.DEFAULT_NAMES:
            p = self.default_config_dir / name
            if p.exists() and p.is_file():
                found.append(p)
        return found

    def _ensure_defaults_present(self) -> List[Path]:
        defaults = self._find_default_files()
        if not defaults:
            raise RuntimeError(
                f"Default config directory '{self.default_config_dir}' does not contain any "
                f"config files (expected one of: {', '.join(self.DEFAULT_NAMES)})"
            )
        return defaults

    def _ensure_user_dir_and_seed(self, defaults: List[Path]) -> None:
        PathHandler(self.user_dir, folder=True)

        finder = ConfigFinder(self.user_dir)
        user_file = finder.find()

        needs_seeding = False
        if user_file is None:
            needs_seeding = True
        else:
            try:
                if user_file.stat().st_size == 0:
                    needs_seeding = True
            except OSError:
                needs_seeding = True

        if needs_seeding:
            copied_any = False
            for src in defaults:
                dst = self.user_dir / src.name
                if not dst.exists():
                    shutil.copyfile(src, dst)
                    copied_any = True
            if not copied_any:
                raise RuntimeError(
                    f"User config in '{self.user_dir}' is missing or empty and seeding from defaults failed."
                )

    def _ensure_schema_present(self) -> Path:
        finder = SchemaFinder(self.schemas_dir)
        schema_path = finder.find_first()
        if schema_path is None:
            raise RuntimeError(
                f"No schema found in '{self.schemas_dir}'. Expected one of: {', '.join(self.DEFAULT_SCHEMAS)}"
            )
        return schema_path

    def load(self) -> Dict[str, Any]:
        defaults = self._ensure_defaults_present()

        self._ensure_user_dir_and_seed(defaults)

        schema_path = self._ensure_schema_present()
        validator = SchemaValidator(schema_path)

        merged_default: Dict[str, Any] = {}
        for name in self.DEFAULT_NAMES:
            src = self.default_config_dir / name
            if src.exists():
                data = ConfigLoader.load(src)
                if isinstance(data, dict):
                    validator.validate(data)
                data = ConfigImporter.expand(data, src.parent, MergeDicts, ConfigLoader)
                MergeDicts.merge(merged_default, data)

        finder = ConfigFinder(self.user_dir)
        user_file = finder.find()
        if not user_file:
            raise RuntimeError(
                f"No user config found in '{self.user_dir}' after seeding."
            )

        user_data = ConfigLoader.load(user_file)
        if isinstance(user_data, dict):
            validator.validate(user_data)
        user_data = ConfigImporter.expand(
            user_data, user_file.parent, MergeDicts, ConfigLoader
        )
        MergeDicts.merge(merged_default, user_data)

        return merged_default
