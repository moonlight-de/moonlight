import platform

from utils.constants import SupportedDistributives
from loguru import logger


class DefineDistro:
    """
    Defines Linux distribution
    """

    @staticmethod
    def get() -> str:
        value: str = SupportedDistributives.LINUX

        try:
            os_info = platform.freedesktop_os_release()
            name = os_info["NAME"]

            for distributiv in SupportedDistributives.DISTRIBUTIVES_LIST:
                if distributiv in name:
                    value = distributiv
                    break

        except Exception:
            logger.warning(
                "Failed to define Linux distribution. Using default. "
                + SupportedDistributives.LINUX
            )
            value = SupportedDistributives.LINUX

        return value
