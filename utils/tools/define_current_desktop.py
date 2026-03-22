from os import environ
from utils.constants import SupportedDesktops


class DefineDesktop:
    """
    Defines Linux desktop environment
    """

    @staticmethod
    def get() -> str:
        env = environ["XDG_CURRENT_DESKTOP"].lower()

        if env in SupportedDesktops.DESKTOPS_LIST:
            return env

        raise ValueError("Unsupported desktop environment.")
