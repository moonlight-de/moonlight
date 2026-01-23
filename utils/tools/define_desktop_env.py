from os import environ


class DefineDesktopEnv:
    """
    Defines Linux desktop environment
    """

    @staticmethod
    def get() -> str:
        SESSION = "wayland"
        return SESSION if environ["XDG_SESSION_TYPE"] == SESSION else "x11"
