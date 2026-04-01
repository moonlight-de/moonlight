from abc import ABC, abstractmethod

from gi.repository import Gtk  # type: ignore
from ignis import widgets
from ignis.utils import Utils

from widgets import config_manager


class BaseBarWidget(ABC):
    """
    Abstract class for status bar widgets
    """

    def __init__(self) -> None:
        self.config = config_manager.statusbar.modules
        self.widget = self.build()
        self._poll = None

        self.update()
        self.start()

    @abstractmethod
    def build(self) -> widgets.Widget | Gtk.Widget:  # type: ignore
        """
        Build the widget here.
        Return a GTK4 or ignis.widgets.Widget.
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Update the widget here.
        """
        raise NotImplementedError

    def start(self) -> None:
        """
        Start internal timers/polls if needed.
        """
        return None

    def refresh_from_config(self, changed_paths: set[str] | None = None) -> None:
        """
        Soft reload hook.
        """
        self.update()

    def destroy(self) -> None:
        """
        Cleanup timers/polls/resources.
        """
        if self._poll is not None:
            cancel = getattr(self._poll, "cancel", None)
            if callable(cancel):
                cancel()
            self._poll = None

    def get_widget(self) -> widgets.Widget | Gtk.Widget:  # type: ignore
        """
        Returns the GTK widget for insertion into a Box
        """
        return self.widget
