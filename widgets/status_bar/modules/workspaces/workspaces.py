from widgets.status_bar.modules.base_widget import BaseBarWidget
from services import WaylandIpcHandler
from ignis import widgets


class WorkspacesWidget(BaseBarWidget):
    def __init__(self):
        self.wayland_ipc = WaylandIpcHandler.create_wayland_ipc()
        super().__init__()

    def build(self):
        return widgets.Label(label="workspaces")

    def update(self):
        pass
