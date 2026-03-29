from __future__ import annotations

from loguru import logger
from watchdog.observers import Observer

from .user_watch_handler import UserStylesWatchHandler
from .user_styles import UserStyles


class UserStylesWatcher:
    def __init__(
        self,
        user_styles: UserStyles,
        handler: UserStylesWatchHandler | None = None,
    ) -> None:
        self.user_styles = user_styles
        self._handler = handler or UserStylesWatchHandler(user_styles)
        self._observer = Observer()

    def start(self) -> None:
        user_style_path = self.user_styles.get_user_style_path()
        if user_style_path is None:
            logger.debug("User stylesheet watcher not started: path is not configured.")
            return

        watch_dir = user_style_path.parent

        if self._observer and self._observer.is_alive():
            return

        self._observer = Observer()
        self._observer.schedule(
            self._handler,
            path=watch_dir.as_posix(),
            recursive=False,
        )
        self._observer.start()

        logger.info(f"Started user stylesheet watcher: {user_style_path}")

    def stop(self) -> None:
        if self._observer and self._observer.is_alive():
            self._observer.stop()
            self._observer.join()
            self._observer = None
            logger.info("Stopped user stylesheet watcher.")
