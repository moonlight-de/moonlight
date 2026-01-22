from pydantic import BaseModel


class MainKeyboardModel(BaseModel):
    address: str
    name: str
    rules: str
    model: str
    layout: str
    variant: str
    options: str
    active_keymap: str
    caps_lock: bool
    num_lock: bool
    main: bool
