from pathlib import Path
from typing import Any, Dict

import jsonschema  # type: ignore

from .loader import ConfigLoader


class SchemaValidator:
    """
    Validates a dict (loaded config) against a JSON Schema.
    Schema itself can be in YAML or JSONC (we use ConfigLoader to load it).
    """

    def __init__(self, schema_path: Path):
        self.schema_path = schema_path
        self.schema: Dict[str, Any] = self._load_schema(schema_path)

    @staticmethod
    def _load_schema(path: Path) -> Dict[str, Any]:
        loaded = ConfigLoader.load(path)
        if not isinstance(loaded, dict):
            raise ValueError(f"Schema at {path} should be a mapping (object).")
        return loaded

    def validate(self, data: Dict[str, Any], raise_exc: bool = True) -> bool:
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            return True
        except jsonschema.ValidationError as e:
            if raise_exc:
                raise
            return False
