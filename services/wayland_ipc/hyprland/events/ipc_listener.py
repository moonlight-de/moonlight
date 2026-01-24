import socket
import threading
import time
from pathlib import Path
import logging

from gi.repository import GLib, GObject  # type: ignore
from ignis.gobject import IgnisGObject
from ignis.utils import listen_socket

log = logging.getLogger(__name__)


class HyprlandIPCListener(IgnisGObject):
    __gsignals__ = {
        "raw-event": (
            GObject.SignalFlags.RUN_FIRST,
            None,
            (str, str),
        ),
    }

    def __init__(self, socket_path: Path) -> None:
        super().__init__()
        self.socket_path = socket_path
        self._running = False

    def start(self) -> None:
        if self._running:
            return

        self._running = True
        threading.Thread(
            target=self._loop,
            daemon=True,
        ).start()

    def _loop(self) -> None:
        while self._running:
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                    sock.connect(self.socket_path.as_posix())
                    log.info("Connected to %s", self.socket_path)

                    for line in listen_socket(sock, errors="ignore"):
                        if not line or ">>" not in line:
                            continue

                        event, payload = line.split(">>", 1)

                        GLib.idle_add(
                            self.emit,
                            "raw-event",
                            event.lower(),
                            payload,
                        )
            except Exception as e:
                log.warning("IPC error: %s", e)
                time.sleep(1)
