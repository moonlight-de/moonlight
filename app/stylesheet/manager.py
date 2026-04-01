from ignis.css_manager import CssInfoPath, CssManager
from loguru import logger

from services.config_reload import config_reload_service
from utils.constants.paths import STYLES_MAIN_FILE, STYLES_USER_FILE

from .scss_compiler import ScssCompiler, ScssWatcher
from .user_styles import UserStyles, UserStylesWatcher


class StylesheetManager:
    def __init__(self) -> None:
        self.css_manager = CssManager.get_default()
        self.compiler = ScssCompiler()
        self.scss_watcher = ScssWatcher(self.compiler)

        self.user_styles = UserStyles()
        self.user_styles_watcher = UserStylesWatcher(self.user_styles)

        self._css_applied = False

        self._scss_watcher_started = False
        self._user_styles_watcher_started = False

        config_reload_service.connect_soft(self._on_soft_reload)

    def setup(self) -> None:
        try:
            self.user_styles.sync()
        except Exception:
            logger.exception("Failed to sync user stylesheet.")

        self.compiler.compile()
        self._apply_css()
        self._start_watchers()

        logger.info("Stylesheet manager initialized.")

    def stop(self) -> None:
        self._stop_watchers()
        logger.info("Stylesheet manager stopped.")

    def _apply_css(self) -> None:
        if self._css_applied:
            return

        self.css_manager.apply_css(
            CssInfoPath(
                name="main-style",
                path=STYLES_MAIN_FILE.as_posix(),
                priority="application",
                autoreload=True,
            )
        )

        self.css_manager.apply_css(
            CssInfoPath(
                name="user-style",
                path=STYLES_USER_FILE.as_posix(),
                priority="application",
                autoreload=True,
            )
        )

        self._css_applied = True

    def _start_watchers(self) -> None:
        if not self._user_styles_watcher_started:
            self.user_styles_watcher.start()
            self._user_styles_watcher_started = True

        if not self._scss_watcher_started:
            self.scss_watcher.start()
            self._scss_watcher_started = True

    def _stop_watchers(self) -> None:
        if self._scss_watcher_started:
            self.scss_watcher.stop()
            self._scss_watcher_started = False

        if self._user_styles_watcher_started:
            self.user_styles_watcher.stop()
            self._user_styles_watcher_started = False

    def reload_styles(self) -> None:
        logger.info("Reloading styles from config changes...")
        self.stop()
        self.setup()

    def _on_soft_reload(self, _config: dict, changed_paths: set[str]) -> None:
        if not any(path.startswith("general.styles.") for path in changed_paths):
            return

        self.reload_styles()
