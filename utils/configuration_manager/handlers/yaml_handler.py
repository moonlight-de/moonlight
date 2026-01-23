from typing import Any, Dict
import yaml

from .config_handler import BaseConfigHandler


class ConfigHandlerYaml(BaseConfigHandler):
    def load(self) -> Dict[str, Any]:
        if not self.path.exists() or self.path.stat().st_size == 0:
            return {}
        raw: Any = yaml.safe_load(self.path.read_text())
        return raw if isinstance(raw, dict) else {}
