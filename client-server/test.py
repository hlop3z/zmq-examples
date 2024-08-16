import threading
import sys
import logging
import time

# Basic
# from basic.client import main as client
# from basic.server import main as server

# Devices
from devices.client import main as client
from devices.server import main as server

# Global variable to control server shutdown
shutdown_event = threading.Event()

# Logging
logging.basicConfig(format="%(levelname)s    —  %(message)s", level=logging.INFO)


def client_wrapper():
    """
    Wrapper for the client function to check for shutdown events.
    """
    while not shutdown_event.is_set():
        client()
        time.sleep(1)  # Adjust sleep if needed


def start_services():
    """
    Starts client and server threads.
    """
    services = [
        threading.Thread(target=client_wrapper),
        threading.Thread(target=server, args=(shutdown_event,)),
    ]

    for thread in services:
        thread.daemon = True  # Make the thread a daemon
        thread.start()

    return services


def main():
    """
    Main function to start services and handle graceful shutdown.
    """
    logging.info("Starting services...")

    services = start_services()

    try:
        while not shutdown_event.is_set():
            time.sleep(1)  # Wait for shutdown event
    except KeyboardInterrupt:
        pass

    logging.info("Stopping services...")
    shutdown_event.set()

    # Wait for threads to finish
    for thread in services:
        thread.join()

    logging.info("Exiting program.")
    sys.exit(0)


if __name__ == "__main__":
    main()
