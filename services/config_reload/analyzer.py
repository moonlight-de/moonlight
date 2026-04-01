from __future__ import annotations

from typing import Any

from utils.constants import (
    HARD_RELOAD_PATHS,
    HARD_RELOAD_PREFIXES,
    SOFT_RELOAD_PREFIXES,
)


class ConfigChangeAnalyzer:
    """
    Responsible only for:
    - finding changed config paths
    - deciding whether reload is soft or hard
    """

    def diff_paths(self, old: Any, new: Any, prefix: str = "") -> set[str]:
        if isinstance(old, dict) and isinstance(new, dict):
            changed: set[str] = set()
            keys = set(old) | set(new)

            for key in keys:
                path = f"{prefix}.{key}" if prefix else str(key)

                if key not in old or key not in new:
                    changed.add(path)
                    continue

                changed |= self.diff_paths(old[key], new[key], path)

            return changed

        if isinstance(old, list) and isinstance(new, list):
            return {prefix} if old != new else set()

        return {prefix} if old != new else set()

    def classify_reload(self, changed_paths: set[str]) -> str | None:
        if not changed_paths:
            return None

        for path in changed_paths:
            if path in HARD_RELOAD_PATHS:
                return "hard"

            if any(path.startswith(prefix) for prefix in HARD_RELOAD_PREFIXES):
                return "hard"

            if (
                path.startswith("widgets.statusbar.modules.")
                and len(path.split(".")) == 4
            ):
                return "hard"

        for path in changed_paths:
            if any(path.startswith(prefix) for prefix in SOFT_RELOAD_PREFIXES):
                return "soft"

        return "hard"
