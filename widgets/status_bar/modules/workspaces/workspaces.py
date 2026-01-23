import json
from widgets.status_bar.modules.base_widget import BaseBarWidget
from services import WaylandIpcHandler


class WorkspacesWidget(BaseBarWidget):
    def __init__(self):
        super().__init__()
        self.wayland_ipc = WaylandIpcHandler.ipc()

    def build(self):
        return self.ignis_widget.Label(label="workspaces")

    def update(self):
        pass
