import threading
import sys
import logging
import time
import signal

# Basic
from basic.sub import main as subscriber
from basic.pub import main as publisher

# Global variable to control server shutdown
shutdown_event = threading.Event()

# Logging
logging.basicConfig(format="%(levelname)s    —  %(message)s", level=logging.INFO)


def pub_wrapper():
    """
    Wrapper for the client function to check for shutdown events.
    """
    while not shutdown_event.is_set():
        publisher()
        time.sleep(1)  # Adjust sleep if needed


def start_services():
    """
    Starts client and server threads.
    """
    services = [
        # threading.Thread(target=device, args=(shutdown_event,)),
        threading.Thread(target=subscriber, args=(shutdown_event,)),
        threading.Thread(target=pub_wrapper),
    ]

    for thread in services:
        thread.daemon = True  # Make the thread a daemon
        thread.start()

    return services


def main():
    """
    Main function to start services and handle graceful shutdown.
    """
    signal.signal(signal.SIGINT, signal.SIG_DFL)

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
