import asyncio
import multiprocessing
import time
import sys
import logging
import os

# ZMQ
import zmq.asyncio

# Logs
logging.basicConfig(format="%(levelname)s    -  %(message)s", level=logging.INFO)


async def server(port):
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{port}")

    print(f"Server running on port {port}")

    while True:
        message = await socket.recv()
        print(f"Received request on port {port}: {message.decode('utf-8')}")
        reply = b"World"
        await socket.send(reply)


def start_server(port):
    # Loop Policy
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run Server
    asyncio.run(server(port))


def main():
    ports = [5555, 5556, 5557]
    processes = []

    logging.info("Starting Server. . .")

    for port in ports:
        process = multiprocessing.Process(target=start_server, args=(port,))
        process.start()
        processes.append(process)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    logging.info("Stopping Server. . .")
    for process in processes:
        process.terminate()
        process.join()

    sys.exit(0)


if __name__ == "__main__":
    main()
