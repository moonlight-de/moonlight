from __future__ import annotations

from pathlib import Path
from typing import Any

import json
import jsonschema

from utils.exceptions import ConfigValidationError


class ConfigValidator:
    def __init__(self, schema_file: Path) -> None:
        self.schema_file = schema_file
        self.schema = self._load_schema(schema_file)

    def _load_schema(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found: {path}")

        raw = path.read_text(encoding="utf-8")
        data = json.loads(raw)

        if not isinstance(data, dict):
            raise ValueError("Schema root must be a JSON object")

        return data

    def validate(self, config: dict[str, Any]) -> None:
        try:
            jsonschema.validate(instance=config, schema=self.schema)
        except jsonschema.ValidationError as e:
            raise ConfigValidationError(
                message=e.message,
                path=[str(p) for p in e.absolute_path],
                validator=e.validator,  # type: ignore
                validator_value=e.validator_value,
            ) from e
