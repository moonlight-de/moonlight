from __future__ import annotations

from pathlib import Path
from typing import Callable

from ignis.utils import Utils
from loguru import logger

from utils.constants import INTERESTING_EVENTS
from utils.tools import PathsHandler


class ConfigWatchRegistry:
    """
    Responsible only for:
    - deciding which paths must be watched
    - creating/removing file monitors
    - filtering filesystem events
    """

    def __init__(
        self,
        get_tracked_files: Callable[[], set[Path]],
        get_backup_file: Callable[[], str | Path],
        on_relevant_change: Callable[[], None],
    ) -> None:
        self._get_tracked_files = get_tracked_files
        self._get_backup_file = get_backup_file
        self._on_relevant_change = on_relevant_change
        self._monitors: dict[Path, object] = {}

    def setup_monitors(self) -> None:
        self.clear_monitors()

        tracked_files = self._tracked_files()
        parent_dirs = {path.parent for path in tracked_files}

        for directory in parent_dirs:
            self._monitors[directory] = Utils.FileMonitor(
                path=str(directory),
                recursive=False,
                callback=self._on_file_changed,
            )

    def clear_monitors(self) -> None:
        for monitor in self._monitors.values():
            cancel = getattr(monitor, "cancel", None)
            if callable(cancel):
                cancel()

        self._monitors.clear()

    def _tracked_files(self) -> set[Path]:
        return {PathsHandler.normalize_path(path) for path in self._get_tracked_files()}

    def _should_react_to_path(self, changed_path: Path) -> bool:
        tracked_files = self._tracked_files()
        backup_path = PathsHandler.normalize_path(self._get_backup_file())

        if changed_path == backup_path:
            return False

        if changed_path.suffix not in {".json", ".jsonc"}:
            return False

        return changed_path in tracked_files

    def _on_file_changed(self, _monitor, path: str, event_type: str) -> None:
        changed_path = PathsHandler.normalize_path(path)

        if event_type not in INTERESTING_EVENTS:
            logger.debug(
                "Config reload skipped: unsupported event={} path={}",
                event_type,
                changed_path,
            )
            return

        if not self._should_react_to_path(changed_path):
            logger.debug(
                "Config reload skipped: untracked path={} event={}",
                changed_path,
                event_type,
            )
            return

        logger.debug("Config source event: {} {}", event_type, changed_path)
        self._on_relevant_change()
