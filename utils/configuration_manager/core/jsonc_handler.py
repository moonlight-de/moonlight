from typing import Any, Dict
import json5

from .config_handler import ConfigHandler


class ConfigHandlerJSONC(ConfigHandler):
    def load(self) -> Dict[str, Any]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return {}
        raw: Any = json5.loads(self.path.read_text())
        return raw if isinstance(raw, dict) else {}
