from __future__ import annotations

from typing import Callable

from services.config_reload import config_reload_service


class ConfigReloadHandler:
    def __init__(
        self,
        on_full_reload: Callable[[set[str]], None],
        on_soft_reload: Callable[[set[str]], None],
        should_full_reload: Callable[[set[str]], bool],
        should_soft_reload: Callable[[set[str]], bool],
    ) -> None:
        self._on_full_reload = on_full_reload
        self._on_soft_reload = on_soft_reload
        self._should_full_reload = should_full_reload
        self._should_soft_reload = should_soft_reload

        config_reload_service.connect_soft(self._dispatch_soft_reload)

    def _dispatch_soft_reload(self, _config: dict, changed_paths: set[str]) -> None:
        if self._should_full_reload(changed_paths):
            self._on_full_reload(changed_paths)
            return

        if self._should_soft_reload(changed_paths):
            self._on_soft_reload(changed_paths)
