from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.jsonc_manager import JSONC

jsonc = JSONC()


class ConfigFileLoader:
    def load(self, path: Path) -> Any:
        if not path.exists():
            return {}
        return jsonc.read(path)
