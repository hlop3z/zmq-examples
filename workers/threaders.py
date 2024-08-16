import threading
import time


class Worker(threading.Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = threading.Event()

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

    time.sleep(5)  # Let the thread run for a bit
    worker.stop()
    worker.join()  # Wait for the thread to finish
    print("Thread terminated")
