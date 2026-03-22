import time


class Debouncer:
    def __init__(self, delay_seconds: float = 0.2) -> None:
        self.delay_seconds = delay_seconds
        self._last_called_at = 0.0

    def is_ready(self) -> bool:
        now = time.monotonic()

        if now - self._last_called_at < self.delay_seconds:
            return False

        self._last_called_at = now
        return True
