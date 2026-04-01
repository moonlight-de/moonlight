from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from ignis.base_service import BaseService
from ignis.utils import Utils
from loguru import logger

from widgets.config import config_manager

from .analyzer import ConfigChangeAnalyzer
from .restarter import ApplicationRestarter
from utils.tools import PathsHandler
from .watcher import ConfigWatchRegistry


ReloadHandler = Callable[[dict[str, Any], set[str]], None]
ErrorHandler = Callable[[Exception], None]


class ConfigReloadService(BaseService):
    """
    Main coordinator.

    Responsibilities:
    - connect handlers
    - orchestrate reload flow
    - delegate analysis/watch/restart to dedicated classes
    """

    def __init__(self) -> None:
        super().__init__()

        self._soft_handlers: list[ReloadHandler] = []
        self._error_handlers: list[ErrorHandler] = []

        self._analyzer = ConfigChangeAnalyzer()
        self._restarter = ApplicationRestarter(
            quit_callback=getattr(self, "quit", None)
        )

        self._last_applied = deepcopy(config_manager.get_config())

        self._debounced_reload = Utils.debounce(300)(self._reload_now)

        self._watch_registry = ConfigWatchRegistry(
            get_tracked_files=self._tracked_files,
            get_backup_file=self._backup_config_file,
            on_relevant_change=self._debounced_reload,
        )

        self._watch_registry.setup_monitors()

    def connect_soft(self, handler: ReloadHandler) -> None:
        self._soft_handlers.append(handler)

    def connect_error(self, handler: ErrorHandler) -> None:
        self._error_handlers.append(handler)

    def _tracked_files(self) -> set[Path]:
        return {
            PathsHandler.normalize_path(path)
            for path in config_manager.get_tracked_config_files()
        }

    def _backup_config_file(self) -> Path:
        return PathsHandler.normalize_path(config_manager.backup_config_file)

    def _emit_soft(
        self,
        config: dict[str, Any],
        changed_paths: set[str],
    ) -> None:
        for handler in tuple(self._soft_handlers):
            try:
                handler(config, changed_paths)
            except Exception:
                logger.exception("Soft reload handler failed")

    def _emit_error(self, error: Exception) -> None:
        for handler in tuple(self._error_handlers):
            try:
                handler(error)
            except Exception:
                logger.exception("Reload error handler failed")

    def _save_backup_config(self, config: dict[str, Any]) -> None:
        save_backup = getattr(config_manager._loader, "save_backup_config", None)
        if callable(save_backup):
            save_backup(config)

    def _reload_now(self) -> None:
        try:
            next_config = config_manager.load_for_runtime_reload()
        except Exception as error:
            logger.warning("Config reload skipped: {}", error)
            self._emit_error(error)
            return

        changed_paths = self._analyzer.diff_paths(self._last_applied, next_config)
        if not changed_paths:
            logger.debug("Config reload finished: effective config unchanged")
            self._watch_registry.setup_monitors()
            return

        reload_kind = self._analyzer.classify_reload(changed_paths)
        logger.info(
            "Config reload kind={} changed_paths={}",
            reload_kind,
            sorted(changed_paths),
        )

        self._last_applied = deepcopy(next_config)
        self._save_backup_config(next_config)

        self._watch_registry.setup_monitors()

        if reload_kind == "soft":
            self._emit_soft(next_config, changed_paths)
            return

        self._restarter.restart()
