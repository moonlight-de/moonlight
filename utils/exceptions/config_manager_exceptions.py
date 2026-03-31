from typing import Any


class ConfigImportError(Exception):
    def pretty(self) -> str:
        lines: list[str] = []
        lines.append("┌─ Config import error")
        lines.append(f"│ Message  : {self}")
        lines.append("└────────────────────────────────────────")
        return "\n".join(lines)


class ConfigImportCycleError(ConfigImportError):
    pass


class ConfigImportNotFoundError(ConfigImportError):
    pass


class ConfigKeyNotFoundError(Exception):
    def __init__(self, path: str) -> None:
        super().__init__(
            f"Config key not found in active, backup, or default config: {path}"
        )
        self.path = path

    def pretty(self) -> str:
        lines: list[str] = []
        lines.append("┌─ Config key not found")
        lines.append(f"│ Path    : {self.path}")
        lines.append("│ Sources : active -> backup -> default")
        lines.append("└────────────────────────────────────────")
        return "\n".join(lines)


class ConfigValidationError(Exception):
    def __init__(
        self,
        message: str,
        path: list[str] | None = None,
        validator: str | None = None,
        validator_value: Any = None,
    ) -> None:
        super().__init__(message)
        self.path = path or []
        self.validator = validator
        self.validator_value = validator_value

    def pretty(self) -> str:
        location = ".".join(self.path) if self.path else "<root>"

        lines: list[str] = []
        lines.append("┌─ Config validation error")
        lines.append(f"│ Path     : {location}")
        lines.append(f"│ Message  : {self}")
        if self.validator:
            lines.append(f"│ Rule     : {self.validator}")
        if self.validator_value is not None:
            lines.append(f"│ Expected : {self.validator_value}")
        lines.append("└────────────────────────────────────────")
        return "\n".join(lines)
