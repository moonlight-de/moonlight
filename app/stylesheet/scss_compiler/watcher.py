from pathlib import Path

from loguru import logger
from watchdog.observers import Observer

from utils.constants.paths import STYLES_SCSS_DIR

from .compiler import ScssCompiler
from .handler import ScssWatchHandler


class ScssWatcher:
    """Manage watchdog observer for SCSS auto compilation."""

    def __init__(
        self,
        compiler: ScssCompiler,
        watch_dir: Path = STYLES_SCSS_DIR,
        handler: ScssWatchHandler | None = None,
    ) -> None:
        self.compiler = compiler
        self.watch_dir = Path(watch_dir).expanduser().resolve()
        self._observer = Observer()
        self._handler = handler or ScssWatchHandler(compiler)

    def _validate_watch_dir(self) -> None:
        if not self.watch_dir.exists():
            raise FileNotFoundError(f"SCSS watch directory not found: {self.watch_dir}")

        if not self.watch_dir.is_dir():
            raise NotADirectoryError(
                f"SCSS watch path is not a directory: {self.watch_dir}"
            )

    def start(self) -> None:
        self._validate_watch_dir()

        self._observer.schedule(
            self._handler,
            path=self.watch_dir.as_posix(),
            recursive=True,
        )
        self._observer.start()

        logger.info(f"Started SCSS watcher: {self.watch_dir}")

    def stop(self) -> None:
        if self._observer.is_alive():
            self._observer.stop()
            self._observer.join()
            logger.info("Stopped SCSS watcher.")
