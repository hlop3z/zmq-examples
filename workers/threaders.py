from abc import ABC, abstractmethod
from types import SimpleNamespace
from typing import Any
import threading
import time


class BaseWorker(threading.Thread, ABC):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.options = SimpleNamespace(**kwargs)
        self._stop_event = threading.Event()

    @abstractmethod
    def server(self):
        """Perform server actions. This method must be implemented by subclasses."""
        pass

    def run(self):
        while not self._stop_event.is_set():
            self.server()

    def stop(self):
        self._stop_event.set()


# Example subclass
class Worker(BaseWorker):
    def server(self):
        print("Working...", self.options)
        time.sleep(1)


# Example usage
if __name__ == "__main__":
    worker = Worker(my_project="one")
    worker.start()

    time.sleep(5)  # Let the thread run for a bit
    worker.stop()
    worker.join()  # Wait for the thread to finish
    print("Thread terminated")
