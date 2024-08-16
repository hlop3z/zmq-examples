import multiprocessing
import time


class Worker(multiprocessing.Process):
    def __init__(self):
        super().__init__()
        self._stop_event = multiprocessing.Event()

    def run(self):
        while not self._stop_event.is_set():
            # Perform your task here
            print("Working...")
            time.sleep(1)

    def stop(self):
        self._stop_event.set()


# Example usage
if __name__ == "__main__":
    worker = Worker()
    worker.start()

    time.sleep(5)  # Let the worker run for a while
    worker.stop()
    worker.join()  # Wait for the worker to finish
    print("Process terminated")
