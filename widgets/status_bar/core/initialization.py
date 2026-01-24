from widgets.status_bar.modules.clock import ClockWidget
from widgets.status_bar.modules.workspaces import WorkspacesWidget


class StatusBarModules:
    """
    List of available modules
    """

    WIDGETS = {
        "clock": ClockWidget,
        "workspaces": WorkspacesWidget,
    }
