from pathlib import Path

from loguru import logger
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from ..debounce import Debouncer
from .user_styles import UserStyles


class UserStylesWatchHandler(FileSystemEventHandler):
    def __init__(self, user_styles: UserStyles) -> None:
        self.user_styles = user_styles
        self.debouncer = Debouncer()

    def _sync(self) -> None:
        if not self.debouncer.is_ready():
            return

        try:
            self.user_styles.sync()
            logger.info("User stylesheet synced after change.")
        except Exception:
            logger.exception("Failed to sync user stylesheet after change.")

    def _resolve_event_path(self, event: FileSystemEvent) -> Path | None:
        if event.is_directory:
            return None

        raw_path = getattr(event, "src_path", None)
        if not raw_path:
            return None

        try:
            return Path(raw_path).expanduser().resolve()
        except Exception:
            return None

    def _matches_current_file(self, event: FileSystemEvent) -> bool:
        current_path = self.user_styles.get_user_style_path()
        event_path = self._resolve_event_path(event)

        if current_path is None or event_path is None:
            return False

        return current_path == event_path

    def on_modified(self, event: FileSystemEvent) -> None:
        if self._matches_current_file(event):
            self._sync()

    def on_created(self, event: FileSystemEvent) -> None:
        if self._matches_current_file(event):
            self._sync()

    def on_deleted(self, event: FileSystemEvent) -> None:
        event_path = self._resolve_event_path(event)
        if event_path is None:
            return

        raw_path = self.user_styles.config.general.get("styles", {}).get(
            "stylesheet_path", ""
        )
        if not raw_path:
            return

        configured_path = Path(raw_path).expanduser().resolve()
        if configured_path == event_path:
            self._sync()

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        raw_path = self.user_styles.config.general.get("styles", {}).get(
            "stylesheet_path", ""
        )
        if not raw_path:
            return

        try:
            configured_path = Path(raw_path).expanduser().resolve()
        except Exception:
            return

        try:
            src_path = Path(event.src_path).expanduser().resolve()
        except Exception:
            src_path = None

        try:
            dest_path = Path(event.dest_path).expanduser().resolve()  # type: ignore[attr-defined]
        except Exception:
            dest_path = None

        if configured_path == src_path or configured_path == dest_path:
            self._sync()
