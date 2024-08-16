import asyncio
import multiprocessing
import time
import sys
import os


# Package
from .device import ZeroMQ


async def server(port):
    # Client Node
    node = ZeroMQ(backend=ZeroMQ.tcp(port))

    # Connect
    node.backend()

    # Server
    print(f"Server running on port {port}")

    while True:
        message = await node.socket.recv()
        print(f"Received request on port {port}: {message.decode('utf-8')}")
        reply = b"World"
        await node.socket.send(reply)


def start_server(port):
    # Loop Policy
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run Server
    asyncio.run(server(port))


def main(shutdown_event):
    ports = [5555]
    processes = []

    # Starting Servers. . .
    for port in ports:
        process = multiprocessing.Process(target=start_server, args=(port,))
        process.start()
        processes.append(process)

    try:
        while not shutdown_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown_event.set()

    # Stopping Servers. . .
    for process in processes:
        process.terminate()
        process.join()

    sys.exit(0)


if __name__ == "__main__":
    stop_event = multiprocessing.Event()
    main(stop_event)
