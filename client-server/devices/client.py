import time
import os
import asyncio

# Package
from manager import ZeroMQ


async def client(port: int):
    # Client Node
    node = ZeroMQ()
    # Client Node
    node = ZeroMQ(frontend=ZeroMQ.tcp(port))

    # Connect
    node.frontend()

    with node.connect() as socket:
        # Request
        request = b"Hello"
        print(f"Sending request to port {port}: {request.decode('utf-8')}")
        await socket.send(request)

        # Response
        reply = await socket.recv()
        print(f"Received reply from port {port}: {reply.decode('utf-8')}")


async def start_clients():
    ports = [5555]
    tasks = [asyncio.create_task(client(port)) for port in ports]
    await asyncio.gather(*tasks)


def main():
    # Loop Policy
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Run Client
    time.sleep(1)
    asyncio.run(start_clients())


if __name__ == "__main__":
    main()
