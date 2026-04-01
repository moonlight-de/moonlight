from ignis import widgets
from loguru import logger
from widgets import config_manager
from .initialization import StatusBarModules


class ModuleHandler:
    """
    sorts modules for the status bar
    """

    def __init__(self):
        layout = config_manager.statusbar.modules_layout.as_dict()
        registry = StatusBarModules.WIDGETS

        self.instances: dict[str, object] = {}
        self.local_modules = {
            "start_widgets": widgets.Box(),
            "center_widgets": widgets.Box(),
            "end_widgets": widgets.Box(),
        }

        for position, modules in layout.items():
            box = self.local_modules.get(position)
            if box is None:
                logger.warning(f"Unknown layout position: {position}")
                continue

            for module_name in modules:
                widget_cls = registry.get(module_name)
                if widget_cls is None:
                    logger.warning(f"Module {module_name} not found.")
                    continue

                module = widget_cls()
                self.instances[module_name] = module
                box.append(module.get_widget())

    def soft_reload(self, changed_paths: set[str]) -> None:
        for module in self.instances.values():
            refresh = getattr(module, "refresh_from_config", None)
            if callable(refresh):
                refresh(changed_paths)

    def destroy(self) -> None:
        for module in self.instances.values():
            destroy = getattr(module, "destroy", None)
            if callable(destroy):
                destroy()

        self.instances.clear()
