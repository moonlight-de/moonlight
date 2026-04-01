from __future__ import annotations

import os
import sys

from loguru import logger


def is_elf_file(path: str) -> bool:
    try:
        with open(path, "rb") as file:
            return file.read(4) == b"\x7fELF"
    except OSError:
        return False


class ApplicationRestarter:
    """
    Responsible only for application restart logic.
    """

    def __init__(self, quit_callback=None) -> None:
        self._quit_callback = quit_callback

    def restart(self) -> None:
        logger.warning("Hard reload detected. Restarting application...")

        if callable(self._quit_callback):
            self._quit_callback()

        if is_elf_file(sys.argv[0]):
            os.execl(sys.argv[0], sys.argv[0], *sys.argv[1:])
        else:
            os.execl(sys.executable, sys.executable, *sys.argv)
