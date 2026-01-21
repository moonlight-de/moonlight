from ignis import widgets

from widgets import config_manager
from utils.constants import APP_NAME
from utils.tools import AnchorHandler
from .core import ModuleHandler


if config_manager.statusbar["enabled"]:

    class StatusBar(widgets.Window):
        """
        Status Bar
        Based from *Window*
        """

        def __init__(self):
            self.modules = ModuleHandler()
            super().__init__(
                title=APP_NAME + "- Status Bar",
                namespace="StatusBar",
                anchor=AnchorHandler.statusbar(config_manager.statusbar["position"]),
                exclusivity="exclusive",
                child=widgets.CenterBox(
                    start_widget=self.modules.local_modules["start_widgets"],
                    center_widget=self.modules.local_modules["center_widgets"],
                    end_widget=self.modules.local_modules["end_widgets"],
                ),
            )
