import asyncio
import os
import time
import threading

# Package
from manager import ZeroMQ


async def device():
    # Device
    node = ZeroMQ()

    # Connect
    node.device()


def run_device():
    # Loop Policy
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run Server
    asyncio.run(device())


def main():
    stop_event = threading.Event()

    # Run Device
    print("Starting DEVICE. . .")
    p = threading.Thread(target=run_device)
    p.start()

    # Let the device run for some time
    try:
        while not stop_event.is_set():
            time.sleep(5)
    except KeyboardInterrupt:
        pass

    # Signal the device to stop
    print("Stopping DEVICE. . .")
    stop_event.set()

    # Wait for the device to finish
    p.join()


if __name__ == "__main__":
    main()
