from .icons import TEXT_ICONS
from .path_handler import PathHandler
from .system import APP_NAME
from .supported_distributive import SupportedDistributives
from .supported_desktops import SupportedDesktops
from .paths import (
    XDG_CONFIG_HOME,
    BACKUP_CONFIG_FILE,
    XDG_CACHE_HOME,
    XDG_DATA_HOME,
    CONFIG_FILE_NAME,
    CONFIG_SCHEMA,
    DEFAULT_CONFIG_FILE,
    STYLES_USER_FILE,
    APP_CONFIG_DIR,
    APP_CACHE_DIR,
    APP_DATA_DIR,
    ROOT_CONFIG_DIR,
    ROOT_SCHEMAS_DIR,
    ETC_DIR,
    STYLES_DIR,
    STYLES_SCSS_DIR,
    STYLES_SCSS_FILE,
    STYLES_MAIN_FILE,
    STYLES_DEFAULT_GTK_FILE,
)


__all__ = [
    "APP_NAME",
    "XDG_CONFIG_HOME",
    "XDG_CACHE_HOME",
    "XDG_DATA_HOME",
    "APP_CONFIG_DIR",
    "APP_CACHE_DIR",
    "APP_DATA_DIR",
    "ROOT_CONFIG_DIR",
    "ROOT_SCHEMAS_DIR",
    "TEXT_ICONS",
    "PathHandler",
    "ETC_DIR",
    "SupportedDistributives",
    "SupportedDesktops",
    "STYLES_DIR",
    "STYLES_SCSS_DIR",
    "STYLES_MAIN_FILE",
    "STYLES_SCSS_FILE",
    "STYLES_DEFAULT_GTK_FILE",
    "STYLES_USER_FILE",
    "CONFIG_SCHEMA",
    "DEFAULT_CONFIG_FILE",
    "CONFIG_FILE_NAME",
    "BACKUP_CONFIG_FILE",
]
