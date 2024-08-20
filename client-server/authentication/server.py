from pathlib import Path
from types import SimpleNamespace
import asyncio
import logging
import multiprocessing
import os
import sys
import time

# ZMQ
import zmq.asyncio
import zmq.auth


def get_certs():
    # Base directory (directory of the current script)
    base_dir = Path(__file__).resolve().parent

    # Directories for certificates, public keys, and private keys
    keys_dir = base_dir / "certificates"
    public_keys_dir = keys_dir / "public_keys"
    secret_keys_dir = keys_dir / "private_keys"

    # Check if the required directories exist
    if not all(
        dir_path.exists() for dir_path in [keys_dir, public_keys_dir, secret_keys_dir]
    ):
        logging.critical("Server `certificates` are missing")
        sys.exit(1)

    def get_key(name):
        secret_key_file = secret_keys_dir / name
        if not secret_key_file.exists():
            logging.error(f"Secret key file {secret_key_file} does not exist")
            sys.exit(1)

        publickey, secretkey = zmq.auth.load_certificate(secret_key_file)
        return publickey, secretkey

    return SimpleNamespace(
        public_keys_dir=public_keys_dir,
        load_certificate=get_key,
    )


async def server(port):
    certs = get_certs()

    # Server
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REP)

    # Certificate
    server_public, server_secret = certs.load_certificate("server.secret")
    socket.curve_publickey = "2x.Y>2(J]I:$7i+CS<BVZMJyXEX)H8?31k5o)?mQ".encode("utf-8")
    socket.curve_secretkey = "B.)wGr$@cYiy(<$ES*$pZ3UmIPEIy+lt1qNY!!Kn".encode("utf-8")
    socket.curve_server = True  # must come before bind

    # Bind
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


def main(shutdown_event):
    ports = [5555]  # , 5556, 5557
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
