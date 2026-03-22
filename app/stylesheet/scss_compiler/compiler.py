from pathlib import Path

from loguru import logger

from utils.constants.paths import STYLES_MAIN_FILE, STYLES_SCSS_FILE

try:
    from dartsass import compile as dart_sass_compile  # type: ignore
except Exception:
    try:
        from dartsass._main import compile as dart_sass_compile  # type: ignore
    except Exception as e:
        raise ImportError(
            "dart-sass package is not available. Install it with your project dependencies."
        ) from e


class ScssCompiler:
    """Compile SCSS entry file into CSS output file using python dart-sass."""

    def __init__(
        self,
        source: Path = STYLES_SCSS_FILE,
        target: Path = STYLES_MAIN_FILE,
    ) -> None:
        self.source = Path(source).expanduser().resolve()
        self.target = Path(target).expanduser().resolve()

    def _validate_source(self) -> None:
        if not self.source.exists():
            raise FileNotFoundError(f"SCSS source file not found: {self.source}")

        if not self.source.is_file():
            raise FileNotFoundError(f"SCSS source path is not a file: {self.source}")

    def _ensure_target_dir(self) -> None:
        self.target.parent.mkdir(parents=True, exist_ok=True)

    def _compile_with_dartsass(self) -> None:
        dart_sass_compile(
            filenames=(
                self.source.as_posix(),
                self.target.as_posix(),
            )
        )

    def compile(self) -> Path:
        self._validate_source()
        self._ensure_target_dir()

        try:
            self._compile_with_dartsass()
            logger.info(f"SCSS compiled successfully: {self.source} -> {self.target}")
            return self.target
        except Exception as e:
            logger.error(f"SCSS compilation error: {e}")
            raise

    def compile_if_changed(self) -> Path | None:
        self._validate_source()
        self._ensure_target_dir()

        if self.target.exists():
            source_mtime = self.source.stat().st_mtime
            target_mtime = self.target.stat().st_mtime

            if target_mtime >= source_mtime:
                logger.debug("SCSS has not changed, skipping compilation.")
                return None

        return self.compile()
