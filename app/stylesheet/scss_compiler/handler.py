from pathlib import Path

from loguru import logger
from watchdog.events import FileSystemEvent, FileSystemEventHandler

from .compiler import ScssCompiler
from app.stylesheet import Debouncer
from .filters import ScssEventFilter


class ScssWatchHandler(FileSystemEventHandler):
    """Watch SCSS changes and recompile the main entry file."""

    def __init__(
        self,
        compiler: ScssCompiler,
    ) -> None:
        self.compiler = compiler
        self.event_filter = ScssEventFilter()
        self.debouncer = Debouncer()

    def _compile(self) -> None:
        if not self.debouncer.is_ready():
            return

        try:
            logger.info("Detected SCSS change, recompiling styles...")
            self.compiler.compile()
        except Exception as e:
            logger.error(f"SCSS watch compilation failed: {e}")

    def on_modified(self, event: FileSystemEvent) -> None:
        if self.event_filter.is_valid_event(event):
            self._compile()

    def on_created(self, event: FileSystemEvent) -> None:
        if self.event_filter.is_valid_event(event):
            self._compile()

    def on_deleted(self, event: FileSystemEvent) -> None:
        if self.event_filter.is_valid_event(event):
            self._compile()

    def on_moved(self, event: FileSystemEvent) -> None:
        if event.is_directory:
            return

        try:
            src_path = Path(str(event.src_path)).expanduser().resolve()
        except Exception:
            src_path = None

        try:
            dest_path = Path(event.dest_path).expanduser().resolve()  # type: ignore[attr-defined]
        except Exception:
            dest_path = None

        if self.event_filter.has_scss_path(src_path, dest_path):
            self._compile()
