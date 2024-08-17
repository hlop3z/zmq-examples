from abc import ABC, abstractmethod
import multiprocessing
import time
from typing import Any
from types import SimpleNamespace


class BaseWorker(multiprocessing.Process, ABC):
    def __init__(self, **kwargs: Any):
        super().__init__()
        self.options = SimpleNamespace(**kwargs)
        self.__stop_event = multiprocessing.Event()

    @abstractmethod
    def server(self):
        """Perform server actions. This method must be implemented by subclasses."""
        pass

    @abstractmethod
    def on_event(self, event_type: str):
        """Run Event"""
        pass

    def run(self):
        """Run Worker"""
        self.on_event("startup")
        while not self.__stop_event.is_set():
            self.server()

    def stop(self):
        """Stop Worker"""
        self.__stop_event.set()
        self.on_event("shutdown")

    @property
    def stop_event(self):
        return self.__stop_event


# Example subclass
class Worker(BaseWorker):
    def server(self):
        print("Working...", self.options)
        time.sleep(1)

    def on_event(self, event_type: str):
        """Run Event"""
        match event_type:
            case "startup":
                print("Starting Server. . .")
            case "shutdown":
                print("Stopping Server. . .")


# Example usage
if __name__ == "__main__":
    worker = Worker(my_project="one")
    worker.start()

    time.sleep(5)  # Let the worker run for a while
    worker.stop()
    worker.join()  # Wait for the worker to finish
    print("Process terminated")
