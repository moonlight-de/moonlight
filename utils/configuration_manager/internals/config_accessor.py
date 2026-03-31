from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..config_manager import ConfigManager


class ConfigNode:
    def __init__(self, manager: ConfigManager, path: str = "") -> None:
        self._manager = manager
        self._path = path

    def _join(self, key: str) -> str:
        return f"{self._path}.{key}" if self._path else key

    def __getattr__(self, key: str) -> ConfigNode:
        if key.startswith("_"):
            raise AttributeError(key)
        return ConfigNode(self._manager, self._join(key))

    def __getitem__(self, key: str) -> ConfigNode:
        return ConfigNode(self._manager, self._join(str(key)))

    @property
    def value(self) -> Any:
        return self._manager.require(self._path)

    def get(self, key: str | None = None, default: Any = None) -> Any:
        path = self._join(key) if key else self._path
        return self._manager.get(path, default=default)

    def require(self, key: str | None = None) -> Any:
        path = self._join(key) if key else self._path
        return self._manager.require(path)

    def has(self, key: str | None = None) -> bool:
        path = self._join(key) if key else self._path
        return self._manager.has(path)

    def as_dict(self) -> dict[str, Any]:
        value = self._manager.require(self._path)
        if not isinstance(value, dict):
            raise TypeError(f"Config value at '{self._path}' is not a dict")
        return value

    def as_list(self) -> list[Any]:
        value = self._manager.require(self._path)
        if not isinstance(value, list):
            raise TypeError(f"Config value at '{self._path}' is not a list")
        return value

    def __bool__(self) -> bool:
        return bool(self._manager.require(self._path))

    def __str__(self) -> str:
        return str(self._manager.require(self._path))

    def __int__(self) -> int:
        return int(self._manager.require(self._path))

    def __float__(self) -> float:
        return float(self._manager.require(self._path))

    def __repr__(self) -> str:
        return (
            f"ConfigNode(path={self._path!r}, value={self._manager.get(self._path)!r})"
        )
