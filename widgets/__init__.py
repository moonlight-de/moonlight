# TODO: config_manager should be imported here
from .config import ConfigWidgetManager

config_manager = ConfigWidgetManager()


# DONE:  ------------------------------------------------
# ┬ ┬┬┌┬┐┌─┐┌─┐┌┬┐┌─┐
# ││││ │││ ┬├┤  │ └─┐
# └┴┘┴─┴┘└─┘└─┘ ┴ └─┘
from .status_bar import StatusBar  # noqa: E402

# DONE:  ------------------------------------------------


__all__ = [
    "config_manager",
    "StatusBar",
]
