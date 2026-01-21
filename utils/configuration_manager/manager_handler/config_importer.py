from pathlib import Path
from typing import TYPE_CHECKING, Any, Set, List
import os

from loguru import logger

if TYPE_CHECKING:
    from ...tools.merge_dicts import MergeDicts  # type: ignore
    from ..manager_handler.config_loader import ConfigLoader  # type: ignore


class ConfigImporter:
    """
    Recursively expand 'import' directives in dicts/lists.
    merge_dict and config_loader are provided by caller (dependency injection).
    """

    @staticmethod
    def _resolve_path(raw: str, base_dir: Path) -> Path:
        p = Path(os.path.expanduser(raw))
        if not p.is_absolute():
            p = (base_dir / p).resolve()
        return p

    @classmethod
    def expand(
        cls,
        data: Any,
        base_dir: Path,
        merge_dict,
        config_loader,
        visited: Set[Path] = None,  # type: ignore
    ) -> Any:
        if visited is None:
            visited = set()

        # --- dict ---
        if isinstance(data, dict):
            if "import" in data:
                raw_import = data["import"]
                import_paths = (
                    raw_import if isinstance(raw_import, list) else [raw_import]
                )
                combined_import: Any = None

                for raw_path in import_paths:
                    imp_path = cls._resolve_path(raw_path, base_dir)
                    if not imp_path.exists() or imp_path in visited:
                        continue
                    visited.add(imp_path)

                    imported = config_loader.load(imp_path)
                    imported = cls.expand(
                        imported, imp_path.parent, merge_dict, config_loader, visited
                    )
                    visited.remove(imp_path)

                    if combined_import is None:
                        combined_import = imported
                    else:
                        if isinstance(combined_import, dict) and isinstance(
                            imported, dict
                        ):
                            merge_dict.merge(combined_import, imported)
                            logger.info(f"Merged config {imp_path} into {base_dir}")
                        elif isinstance(combined_import, list) and isinstance(
                            imported, list
                        ):
                            combined_import.extend(imported)
                        else:
                            if not isinstance(combined_import, list):
                                combined_import = [combined_import]
                            combined_import.append(imported)

                # If dict only had "import", return imported content directly
                if set(data.keys()) == {"import"}:
                    return combined_import

                # Merge imported dict(s) into current dict (current keys override)
                result_base = (
                    dict(combined_import) if isinstance(combined_import, dict) else {}
                )
                for k, v in data.items():
                    if k != "import":
                        result_base[k] = cls.expand(
                            v, base_dir, merge_dict, config_loader, visited
                        )
                return result_base

            # No import key: recurse into children
            return {
                k: cls.expand(v, base_dir, merge_dict, config_loader, visited)
                for k, v in data.items()
            }

        # --- list ---
        if isinstance(data, list):
            new_list: List[Any] = []
            for item in data:
                if isinstance(item, dict) and "import" in item:
                    expanded = cls.expand(
                        item, base_dir, merge_dict, config_loader, visited
                    )
                    if isinstance(expanded, list):
                        new_list.extend(expanded)
                    else:
                        new_list.append(expanded)
                else:
                    new_list.append(
                        cls.expand(item, base_dir, merge_dict, config_loader, visited)
                    )
            return new_list

        # primitive
        return data
