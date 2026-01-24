from pydantic import BaseModel


class WorkspaceModel(BaseModel):
    name: str
    monitor: str
    monitor_id: int
    windows: int
    has_fullscreen: bool
