from abc import ABC, abstractmethod

from gi.repository import Gtk  # type: ignore
from ignis import widgets

from widgets import config_manager


class BaseBarWidget(ABC):
    def __init__(self) -> None:
        self.config_manager = config_manager
        self.config = config_manager.statusbar.modules
        self.widget: widgets.Widget | Gtk.Widget | None = None  # type: ignore
        self._poll = None

        self.on_init()

        self.widget = self.build()
        self.update()
        self.start()

    def on_init(self) -> None:
        """
        Optional child initialization hook.
        Runs before build().
        """
        return None

    @abstractmethod
    def build(self) -> widgets.Widget | Gtk.Widget:  # type: ignore
        raise NotImplementedError

    @abstractmethod
    def update(self, *_args) -> None:
        raise NotImplementedError

    def start(self) -> None:
        return None

    def refresh_from_config(self, changed_paths: set[str] | None = None) -> None:
        self.update()

    def destroy(self) -> None:
        if self._poll is not None:
            cancel = getattr(self._poll, "cancel", None)
            if callable(cancel):
                cancel()
            self._poll = None

    def get_widget(self) -> widgets.Widget | Gtk.Widget:  # type: ignore
        if self.widget is None:
            raise RuntimeError(f"{self.__class__.__name__} is not initialized.")
        return self.widget
