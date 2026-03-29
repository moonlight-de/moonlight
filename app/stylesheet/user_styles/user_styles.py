from pathlib import Path

from loguru import logger
from widgets import config_manager

from utils.constants.paths import STYLES_USER_FILE


class UserStyles:
    def __init__(self) -> None:
        self.config = config_manager

    def get_user_style_path(self) -> Path | None:
        raw_path = self.config.general.get("styles", {}).get("stylesheet_path", "")

        if not raw_path:
            return None

        path = Path(raw_path).expanduser()

        if not path.exists() or not path.is_file():
            return None

        return path.resolve()

    def sync(self) -> Path:
        STYLES_USER_FILE.parent.mkdir(parents=True, exist_ok=True)

        user_style_path = self.get_user_style_path()

        if user_style_path is None:
            STYLES_USER_FILE.write_text("", encoding="utf-8")
            logger.debug("User stylesheet not configured or invalid.")
            return STYLES_USER_FILE

        content = user_style_path.read_text(encoding="utf-8")
        STYLES_USER_FILE.write_text(content, encoding="utf-8")

        logger.info(f"Loaded user stylesheet: {user_style_path}")
        return STYLES_USER_FILE
