from widgets.status_bar.modules.base_widget import BaseBarWidget
from ignis import widgets


class WorkspacesWidget(BaseBarWidget):
    def on_init(self) -> None:
        self.events = self.config_manager.wayland_ipc.events.workspace
        self.workspace_service = self.config_manager.wayland_ipc.workspace

        self.events.changed(self.update)

    def build(self):
        self.child_box = widgets.Box()
        self.label = widgets.Label(
            label=str(self.workspace_service.active_workspace_id)
        )
        self.child_box.append(self.label)

        return self.child_box

    def update(self, *_args):
        self.label.set_text(str(self.workspace_service.active_workspace_id))
