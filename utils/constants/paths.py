import os
from pathlib import Path

from gi.repository import GLib  # type: ignore

from utils.constants import APP_NAME


PROJECT_ROOT = Path(__file__).parent.parent.parent
HOME = Path.home()

# Basic XDG Variables
XDG_CONFIG_HOME = Path(os.getenv("XDG_CONFIG_HOME", GLib.get_user_config_dir()))
XDG_CACHE_HOME = Path(os.getenv("XDG_CACHE_HOME", GLib.get_user_cache_dir()))
XDG_DATA_HOME = Path(os.getenv("XDG_DATA_HOME", GLib.get_user_data_dir()))
XDG_RUNTIME_DIR = Path(os.getenv("XDG_RUNTIME_DIR", GLib.get_user_runtime_dir()))

# App Paths
APP_CONFIG_DIR = XDG_CONFIG_HOME / APP_NAME
APP_CACHE_DIR = XDG_CACHE_HOME / APP_NAME
APP_DATA_DIR = XDG_DATA_HOME / APP_NAME

# Configuration Paths
ROOT_CONFIG_DIR = PROJECT_ROOT / "config"
ROOT_SCHEMAS_DIR = ROOT_CONFIG_DIR / "schemas"

# configuration defaults
CONFIG_DEFAULT_SCHEMAS = ("schema.yaml", "schema.yml", "schema.jsonc")
CONFIG_DEFAULT_NAMES = ("config.yaml", "config.yml", "config.jsonc")

# system configuration
ETC_DIR = Path("/etc")

# styles
STYLES_DIR = PROJECT_ROOT / "styles"
STYLES_SCSS_DIR = STYLES_DIR / "scss"
STYLES_SCSS_FILE = STYLES_SCSS_DIR / "import.scss"
STYLES_MAIN_FILE = STYLES_DIR / "main.css"
STYLES_DEFAULT_GTK_FILE = STYLES_DIR / "default_gtk_theme" / "default_gtk.css"
