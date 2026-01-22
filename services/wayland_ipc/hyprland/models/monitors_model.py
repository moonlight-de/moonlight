from typing import List, Optional
from pydantic import BaseModel


class MonitorsModel(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    serial: Optional[str] = None
    width: int
    height: int
    physical_width: Optional[int] = None
    physical_height: Optional[int] = None
    refresh_rate: Optional[float] = None
    scale: float = 1.0
    focused: bool = False
    available_modes: Optional[List[str]] = None
