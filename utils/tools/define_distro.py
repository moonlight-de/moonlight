import platform

from utils.constants import Distributives
from loguru import logger


class DefineDistro:
    """
    Defines Linux distribution
    """

    @staticmethod
    def get() -> str:
        value: str = Distributives.LINUX

        try:
            os_info = platform.freedesktop_os_release()
            name = os_info["NAME"]

            for distributiv in Distributives.DISTRIBUTIVES:
                if distributiv in name:
                    value = distributiv
                    break

        except Exception:
            logger.warning(
                "Failed to define Linux distribution. Using default. "
                + Distributives.LINUX
            )
            value = Distributives.LINUX

        return value
