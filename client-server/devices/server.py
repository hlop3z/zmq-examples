import asyncio
import multiprocessing
import time
import sys
import os


# Package
from .manager import ZeroMQ


async def server(uid):
    # Client Node
    # backend=ZeroMQ.tcp(port)
    node = ZeroMQ()

    # Connect
    # node.device()
    node.backend(True)

    # Server
    print(f"Server running ID: {uid}")

    while True:
        message = await node.socket.recv()
        print(f"Server ID {uid} Received: {message.decode('utf-8')}")
        reply = f"World from {uid}"
        await node.socket.send(reply.encode("utf-8"))


def start_server(port):
    # Loop Policy
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run Server
    asyncio.run(server(port))


def main(shutdown_event):
    total_count = 4
    processes = []

    # Starting Servers. . .
    for uid in range(total_count):
        process = multiprocessing.Process(target=start_server, args=(uid,))
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
