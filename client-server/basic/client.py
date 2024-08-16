import os
import asyncio

# ZMQ
import zmq.asyncio


async def client(port: int, timeout: int = 5000):
    # Connect
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(f"tcp://localhost:{port}")

    # Timeout
    socket.setsockopt(zmq.RCVTIMEO, timeout)
    socket.setsockopt(zmq.SNDTIMEO, timeout)

    # Request
    request = b"Hello"
    print(f"Sending request to port {port}: {request.decode('utf-8')}")
    await socket.send(request)

    # Response
    reply = await socket.recv()
    print(f"Received reply from port {port}: {reply.decode('utf-8')}")


async def start_clients():
    ports = [5555, 5556, 5557]
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
