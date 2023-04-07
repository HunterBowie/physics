import threading
import time
from typing import Callable


class Timer:
    """
    A class for calculating time in seconds.
    """

    def __init__(self):
        self.reset()

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.get()}"

    def start(self):
        """
        Sets the timer relative to now.
        """
        self.start_time = time.monotonic()
        self.stop_time = -1

    def reset(self):
        """
        Sets the timer to always read zero.
        """
        self.start_time = -1
        self.stop_time = -1

    def stop(self):
        """
        Sets the timer stop value to now.
        """
        self.stop_time = time.monotonic()

    def get(self) -> int:
        """
        Returns the difference between now
        and start value. If stop() is called,
        then it returns the difference between
        start and stop times.
        """
        if self.start_time == -1:
            return 0
        if self.stop_time == -1:
            return time.monotonic() - self.start_time

        return self.stop_time - self.start_time

    def passed(self, seconds: int) -> bool:
        """
        Returns true if the timer has exceeded
        the given time.
        """
        return self.get() >= seconds

    def stopped(self) -> bool:
        "Check if the timer has been stopped."
        return self.stop_time != -1

    def started(self) -> bool:
        return self.start_time != -1

    def _trigger(self, function: Callable[[], None], seconds: int):
        timer = Timer()
        timer.start()
        while not timer.passed(seconds):
            pass
        function.__call__()

    def trigger(self, function: Callable[[], None], seconds: int):
        threading.Thread(target=self._trigger, args=(function, seconds)).start()
