from pathlib import Path

from watchdog.events import FileSystemEvent


class ScssEventFilter:
    def is_valid_event(self, event: FileSystemEvent) -> bool:
        if event.is_directory:
            return False

        try:
            event_path = Path(str(event.src_path)).expanduser().resolve()
        except Exception:
            return False

        if event_path.suffix != ".scss":
            return False

        name = event_path.name
        if name.startswith(".") or name.endswith("~") or name.endswith(".tmp"):
            return False

        return True

    def has_scss_path(self, *paths: Path | None) -> bool:
        for path in paths:
            if path is None:
                continue

            if path.suffix == ".scss":
                return True

        return False
