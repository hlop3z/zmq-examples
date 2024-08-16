from abc import ABC, abstractmethod
import multiprocessing
import time
from typing import Any
from types import SimpleNamespace


class BaseWorker(multiprocessing.Process, ABC):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.options = SimpleNamespace(**kwargs)
        self._stop_event = multiprocessing.Event()

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

    time.sleep(5)  # Let the worker run for a while
    worker.stop()
    worker.join()  # Wait for the worker to finish
    print("Process terminated")
