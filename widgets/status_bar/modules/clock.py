import time
from .base_widget import BarWidget


class ClockWidget(BarWidget):
    """
    Display the current time
    Based *BarWidget
    """

    def __init__(self) -> None:
        super().__init__()

    def build(self):
        return self.ignis_widget.Label()

    def update(self):
        self.ignis_utils.Poll(
            timeout=1_000,
            callback=lambda s: self.widget.set_text(
                time.strftime(
                    self.config["clock"]["format"],
                )
            ),
        )
