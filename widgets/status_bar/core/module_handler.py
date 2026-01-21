from ignis import widgets
from loguru import logger
from widgets import config_manager
from .initialization import StatusBarModules


class ModuleHandler:
    """
    sorts modules for the status bar
    """

    def __init__(self):
        layout = config_manager.statusbar["modules_layout"]
        registry = StatusBarModules.WIDGETS

        self.local_modules = {
            "start_widgets": widgets.Box(),
            "center_widgets": widgets.Box(),
            "end_widgets": widgets.Box(),
        }

        for position, modules in layout.items():
            box = self.local_modules[position]
            if not box:
                logger.warning(f"Unknown layout position: {position}")
                continue

            for module_name in modules:
                widget_cls = registry[module_name]
                if not widget_cls:
                    logger.warning(f"Module {module_name} not found.")
                    continue

                box.append(widget_cls().get_widget())
