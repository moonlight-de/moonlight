from ignis import widgets

from widgets import config_manager
from utils.constants import APP_NAME
from utils.tools import AnchorHandler
from utils.config_reload_handler import ConfigReloadHandler
from .core import ModuleHandler


class StatusBar(widgets.Window):
    """
    Status Bar
    Based from Window
    """

    def __init__(self):
        self.modules: ModuleHandler | None = None
        self._reload_handler: ConfigReloadHandler | None = None

        super().__init__(
            title=APP_NAME + "- Status Bar",
            namespace="StatusBar",
            exclusivity="exclusive",
            anchor=[],
            child=widgets.Box(),
        )

        # --------- Dynamic Reloading ---------

        self._reload_handler = ConfigReloadHandler(
            on_full_reload=self._handle_full_reload,
            on_soft_reload=self._handle_soft_reload,
            should_full_reload=self._should_full_reload,
            should_soft_reload=self._should_soft_reload,
        )

        self.reload()

    def _build_child(self):
        self.modules = ModuleHandler()

        return widgets.CenterBox(
            start_widget=self.modules.local_modules["start_widgets"],
            center_widget=self.modules.local_modules["center_widgets"],
            end_widget=self.modules.local_modules["end_widgets"],
        )

    def reload(self) -> None:
        enabled = config_manager.statusbar.enabled.value

        if self.modules is not None:
            self.modules.destroy()
            self.modules = None

        if not enabled:
            self.set_child(None)
            self.set_visible(False)
            return

        self.anchor = AnchorHandler.statusbar(config_manager.statusbar.position.value)

        self.set_child(self._build_child())
        self.set_visible(True)

    def _should_full_reload(self, changed_paths: set[str]) -> bool:
        return any(
            path.startswith("widgets.statusbar.modules_layout.")
            for path in changed_paths
        )

    def _should_soft_reload(self, changed_paths: set[str]) -> bool:
        return any(
            path.startswith("widgets.statusbar.modules.") for path in changed_paths
        )

    def _handle_full_reload(self, _changed_paths: set[str]) -> None:
        self.reload()

    def _handle_soft_reload(self, changed_paths: set[str]) -> None:
        if self.modules is None:
            return

        self.modules.soft_reload(changed_paths)
