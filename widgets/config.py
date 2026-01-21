from utils import (
    ConfigManager,
)

from utils.constants import (
    ROOT_SCHEMAS_DIR,
    ROOT_CONFIG_DIR,
    APP_CONFIG_DIR,
)


class ConfigWidgetManager(ConfigManager):
    """
    Initialize the config manager
    """

    def __init__(self):
        super().__init__(
            APP_CONFIG_DIR,
            ROOT_CONFIG_DIR,
            ROOT_SCHEMAS_DIR,
        )
        self.config = self.load()
        self.general = self.config["general"]
        self.widgets = self.config["widgets"]
        self.statusbar = self.widgets["statusbar"]
