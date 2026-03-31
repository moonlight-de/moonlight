from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from loguru import logger
from utils.exceptions import (
    ConfigImportCycleError,
    ConfigImportError,
    ConfigImportNotFoundError,
)


class ConfigImportResolver:
    def __init__(self, loader: Any, merger: Any) -> None:
        self.loader = loader
        self.merger = merger

    def resolve(self, data: Any, base_dir: Path) -> Any:
        return self._resolve(data, base_dir, visited=set())

    def _resolve(
        self,
        data: Any,
        base_dir: Path,
        visited: set[Path],
    ) -> Any:
        if isinstance(data, dict):
            return self._resolve_dict(data, base_dir, visited)

        if isinstance(data, list):
            return self._resolve_list(data, base_dir, visited)

        return data

    def _resolve_dict(
        self,
        data: dict[str, Any],
        base_dir: Path,
        visited: set[Path],
    ) -> Any:
        if "import" not in data:
            return {
                key: self._resolve(value, base_dir, visited)
                for key, value in data.items()
            }

        raw_import = data["import"]
        import_items = raw_import if isinstance(raw_import, list) else [raw_import]

        combined_import: Any = None

        for raw_path in import_items:
            if not isinstance(raw_path, str):
                raise ConfigImportError(
                    f"Import value must be a string or list of strings, got: {type(raw_path).__name__}"
                )

            imp_path = self._resolve_path(raw_path, base_dir)

            if not imp_path.exists():
                raise ConfigImportNotFoundError(
                    f"Imported config not found: {imp_path}"
                )

            if imp_path in visited:
                raise ConfigImportCycleError(f"Cyclic import detected for: {imp_path}")

            visited.add(imp_path)
            try:
                imported = self.loader.load(imp_path)
                imported = self._resolve(imported, imp_path.parent, visited)
            finally:
                visited.remove(imp_path)

            logger.info("Imported config from {}", imp_path)

            if combined_import is None:
                combined_import = imported
            else:
                combined_import = self._merge_imported_values(
                    combined_import,
                    imported,
                    imp_path,
                )

        if set(data.keys()) == {"import"}:
            return combined_import if combined_import is not None else {}

        local_data = {
            key: self._resolve(value, base_dir, visited)
            for key, value in data.items()
            if key != "import"
        }

        if combined_import is None:
            return local_data

        if isinstance(combined_import, dict) and isinstance(local_data, dict):
            return self.merger.merge(base=combined_import, override=local_data)

        return local_data

    def _resolve_list(
        self,
        data: list[Any],
        base_dir: Path,
        visited: set[Path],
    ) -> list[Any]:
        result: list[Any] = []

        for item in data:
            if isinstance(item, dict) and "import" in item:
                expanded = self._resolve(item, base_dir, visited)
                if isinstance(expanded, list):
                    result.extend(expanded)
                else:
                    result.append(expanded)
            else:
                result.append(self._resolve(item, base_dir, visited))

        return result

    def _merge_imported_values(
        self,
        current: Any,
        new: Any,
        imported_path: Path,
    ) -> Any:
        if isinstance(current, dict) and isinstance(new, dict):
            merged = self.merger.merge(base=current, override=new)
            logger.info("Merged imported dict {}", imported_path)
            return merged

        if isinstance(current, list) and isinstance(new, list):
            logger.info("Extended imported list {}", imported_path)
            return [*current, *new]

        if not isinstance(current, list):
            current = [current]

        current.append(new)
        logger.info("Appended imported value {}", imported_path)
        return current

    @staticmethod
    def _resolve_path(raw: str, base_dir: Path) -> Path:
        path = Path(os.path.expanduser(raw))
        if not path.is_absolute():
            path = (base_dir / path).resolve()
        return path
