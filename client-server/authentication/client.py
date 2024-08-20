from pathlib import Path
from types import SimpleNamespace
import asyncio
import logging
import os
import sys


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
        logging.critical("Client `certificates` are missing")
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


async def client(port: int, timeout: int = 5000):
    certs = get_certs()

    # Connect
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REQ)

    # Timeout
    socket.setsockopt(zmq.RCVTIMEO, timeout)
    socket.setsockopt(zmq.SNDTIMEO, timeout)

    # Authenticator
    client_public, client_secret = certs.load_certificate("client.secret")
    socket.curve_publickey = "1oQj?Q{i3#54qr)EZDx^:9O]jkCf9rfFWrhX(Ilg".encode("utf-8")
    socket.curve_secretkey = "KQ}<GYmCZna=jmL8!REG1k)JMzJ7OTGu)j<*Xdp?".encode("utf-8")

    # The client must know the server's public key to make a CURVE connection.
    server_public_file = certs.public_keys_dir / "server.key"
    server_public, _ = zmq.auth.load_certificate(server_public_file)
    socket.curve_serverkey = "2x.Y>2(J]I:$7i+CS<BVZMJyXEX)H8?31k5o)?mQ".encode("utf-8")

    # Connect
    socket.connect(f"tcp://localhost:{port}")

    # Request
    request = b"Hello"
    print(f"Sending request to port {port}: {request.decode('utf-8')}")
    await socket.send(request)

    # Response
    reply = await socket.recv()
    print(f"Received reply from port {port}: {reply.decode('utf-8')}")


async def start_clients():
    ports = [5555]  # , 5556, 5557
    tasks = [asyncio.create_task(client(port)) for port in ports]
    await asyncio.gather(*tasks)


def main():
    # Loop Policy
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run Client
    asyncio.run(start_clients())


if __name__ == "__main__":
    main()
