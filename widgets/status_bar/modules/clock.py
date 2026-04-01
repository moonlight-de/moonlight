import time

from .base_widget import BaseBarWidget
from ignis import widgets
from ignis.utils import Utils


class ClockWidget(BaseBarWidget):
    """
    Display the current time
    Based on BaseBarWidget
    """

    def build(self):
        return widgets.Label()

    def start(self) -> None:
        self._poll = Utils.Poll(
            timeout=1_000,
            callback=lambda _: self.update(),
        )

    def update(self) -> None:
        self.widget.set_text(  # type: ignore[attr-defined]
            time.strftime(self.config.clock.format.value)
        )

    def refresh_from_config(self, changed_paths: set[str] | None = None) -> None:
        if changed_paths is not None:
            if "widgets.statusbar.modules.clock.format" not in changed_paths:
                return

        self.update()
