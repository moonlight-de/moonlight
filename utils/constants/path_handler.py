from pathlib import Path


class PathHandler:
    """
    Determines whether the path is a file or folder,
    and creates them if necessary.
    """

    def __init__(
        self,
        path: Path,
        folder: bool = False,
        file: bool = False,
    ) -> None:
        self.path = path

        if folder and file:
            raise ValueError("Path cannot be both folder and file.")

        self.folder = folder
        self.file = file

        self._path_type()

        self.ensure_exists()

    def _path_type(self) -> None:
        """
        Determines whether the path is a file or folder
        """
        if self.path.exists():
            self.folder = self.path.is_dir()
            self.file = self.path.is_file()
        else:
            if not self.folder and not self.file:
                if self.path.suffix:
                    self.file = True
                    self.folder = False
                else:
                    self.folder = True
                    self.file = False

    def ensure_exists(self) -> None:
        """
        Creates the path if it doesn't exist
        """
        try:
            if self.folder:
                self.path.mkdir(parents=True, exist_ok=True)
            elif self.file:
                self.path.parent.mkdir(parents=True, exist_ok=True)
                self.path.touch(exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Cannot create path {self.path}: {e}")

    def __repr__(self) -> str:
        return f"<PathHandler path={self.path} folder={self.folder} file={self.file}>"
