from pathlib import Path


class PathsHandler:
    @staticmethod
    def normalize_path(path: str | Path) -> Path:
        return Path(path).expanduser().resolve(strict=False)
