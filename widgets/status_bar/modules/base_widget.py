from abc import ABC, abstractmethod
from widgets import config_manager
from gi.repository import Gtk, GLib  # type: ignore
from ignis import widgets
from ignis import utils
from ignis.services import hyprland, niri


class BarWidget(ABC):
    """
    Abstract class for status bar widgets
    """

    def __init__(self) -> None:
        self.config = config_manager.statusbar["modules"]
        self.ignis_utils = utils
        self.ignis_widget = widgets
        self.ignis_hyprland = hyprland
        self.ignis_niri = niri

        self.widget = self.build()
        GLib.idle_add(self.update)

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

    ...

    def get_widget(self) -> widgets.Widget | Gtk.Widget:  # type: ignore
        """
        Returns the GTK widget for insertion into a Box
        """
        return self.widget
