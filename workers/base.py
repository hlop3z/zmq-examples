from abc import ABC, abstractmethod
import multiprocessing
import time
from typing import Any
from types import SimpleNamespace
import threading


class AbstractWorker(ABC):
    def __init__(self, **kwargs: Any):
        self.options = SimpleNamespace(**kwargs)
        self.__stop_event = self._start_event()

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

    @abstractmethod
    def _start_event(self):
        """Create a stop event. This method must be implemented by subclasses."""
        pass


class BaseProcess(AbstractWorker, multiprocessing.Process):
    def __init__(self, **kwargs: Any):
        multiprocessing.Process.__init__(self)
        AbstractWorker.__init__(self, **kwargs)

    def _start_event(self):
        return multiprocessing.Event()


class BaseThread(AbstractWorker, threading.Thread):
    def __init__(self, **kwargs: Any):
        threading.Thread.__init__(self)
        AbstractWorker.__init__(self, **kwargs)

    def _start_event(self):
        return threading.Event()


# Example subclass
class Shared:
    def on_event(self, event_type: str):
        """Run Event"""
        match event_type:
            case "startup":
                print("Starting Server. . .")
            case "shutdown":
                print("Stopping Server. . .")


class WorkerOne(Shared, BaseProcess):
    def server(self):
        print("Process Working...", self.options)
        time.sleep(1)


class WorkerTwo(Shared, BaseThread):
    def server(self):
        print("Thread Working...", self.options)
        time.sleep(1)


class BaseServer(ABC):
    """
    Control multiple worker `Thread(s)` and/or `Process(es)`.
    """

    workers: list[Any] = []
    on_event: Any

    @classmethod
    def add(cls, *workers: list[Any]) -> None:
        """
        Add worker instances to the service.
        """
        cls.workers.extend(workers)

    @classmethod
    def start(cls, is_loop: bool = True) -> None:
        """
        Start all added workers and optionally keep the main thread running until interrupted.
        """
        # Startup
        cls.on_event("startup")
        for worker in cls.workers:
            worker.start()

        # Loop Until (Keyboard-Interrupt)
        if is_loop:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                cls.stop()

        # Shutdown
        cls.on_event("shutdown")

    @classmethod
    def stop(cls, cleanup: bool = False) -> None:
        """
        Stop all running workers and optionally remove workers.
        """
        for worker in cls.workers:
            worker.stop()
        # Process & Threads
        for worker in cls.workers:
            if hasattr(worker, "terminate"):
                worker.terminate()
            worker.join()
        # Cleanup
        if cleanup:
            cls.workers.clear()


class Service(BaseServer):
    """Service"""

    @staticmethod
    def on_event(event_type: str):
        """Run Event"""
        print(event_type)


Worker = WorkerTwo

# Example usage
if __name__ == "__main__":
    Service.add(
        Worker(my_project="one"),
        Worker(my_project="two"),
    )

    # Start
    Service.start()
    # Let the worker run for a while
    # time.sleep(5)
    # Stop
    # Service.stop()

    print("Worker terminated")
