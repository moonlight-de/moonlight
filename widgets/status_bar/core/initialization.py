from widgets.status_bar.modules import ClockWidget
from widgets.status_bar.modules import WorkspacesWidget


class StatusBarModules:
    """
    List of available modules
    """

    WIDGETS = {
        "clock": ClockWidget,
        "workspaces": WorkspacesWidget,
    }
