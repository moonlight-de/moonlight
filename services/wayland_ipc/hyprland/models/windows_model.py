from pydantic import BaseModel
from typing import Tuple


class WindowsModel(BaseModel):
    address: str
    at: Tuple[int, int]
    size: Tuple[int, int]
    workspace_id: int
    floating: bool
    monitor: int
    monitor_id: int
    class_name: str
    title: str
    initial_title: str
    pid: int
    pinned: bool
    fullscreen: bool
