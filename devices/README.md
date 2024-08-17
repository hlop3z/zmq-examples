Using `zmq.devices.ProcessDevice` allows you to create devices that run in separate processes, providing isolation and potentially better performance in some scenarios. Here, we'll cover three examples using `zmq.devices.ProcessDevice` for different patterns: `Queue`, `Forwarder`, and `Streamer`.

---

---

---

### 1. `Queue` for (`Request` and `Response`)

A `Queue` device forwards messages between frontend and backend sockets. This is useful for request-response patterns.

**Broker (queue_broker.py):**

```python
import zmq
from zmq.devices import ProcessDevice

def main():
    # Create a ProcessDevice for QUEUE
    queue_device = ProcessDevice(zmq.QUEUE, zmq.ROUTER, zmq.DEALER)

    # Bind the frontend socket to receive client requests
    queue_device.bind_in("tcp://*:5555")

    # Bind the backend socket to send requests to workers
    queue_device.bind_out("tcp://*:5556")

    # Start the device
    queue_device.start()

    print("Queue broker started, waiting for clients and workers...")

if __name__ == "__main__":
    main()
```

**Client (client.py):**

```python
import zmq

def main():
    context = zmq.Context()

    # Create a REQ socket to send requests to the broker
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Send a request to the broker
    request = b"Hello"
    print(f"Client sending request: {request}")
    socket.send(request)

    # Wait for a response from the broker
    response = socket.recv()
    print(f"Client received response: {response}")

if __name__ == "__main__":
    main()
```

**Worker (worker.py):**

```python
import zmq

def main():
    context = zmq.Context()

    # Create a REP socket to receive requests from the broker
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5556")

    while True:
        # Wait for a request from the broker
        request = socket.recv()
        print(f"Worker received request: {request}")

        # Process the request
        response = b"World"

        # Send the response back to the broker
        socket.send(response)

if __name__ == "__main__":
    main()
```

---

---

---

### 2. `Forwarder` for (`Publisher` and `Subscriber`)

A `Forwarder` device forwards messages from one socket to another, typically used in publish-subscribe patterns.

**Forwarder (forwarder.py):**

```python
import zmq
from zmq.devices import ProcessDevice

def main():
    # Create a ProcessDevice for FORWARDER
    forwarder_device = ProcessDevice(zmq.FORWARDER, zmq.SUB, zmq.PUB)

    # Bind the frontend socket to receive messages from publishers
    forwarder_device.bind_in("tcp://*:5555")
    forwarder_device.setsockopt_in(zmq.SUBSCRIBE, b"")

    # Bind the backend socket to forward messages to subscribers
    forwarder_device.bind_out("tcp://*:5556")

    # Start the device
    forwarder_device.start()

    print("Forwarder started, forwarding messages from publishers to subscribers...")

if __name__ == "__main__":
    main()
```

**Publisher (publisher.py):**

```python
import zmq
import time

def main():
    context = zmq.Context()

    # Create a PUB socket to send messages to the forwarder
    socket = context.socket(zmq.PUB)
    socket.connect("tcp://localhost:5555")

    while True:
        # Send a message to the forwarder
        message = b"Hello, World!"
        print(f"Publisher sending message: {message}")
        socket.send(message)

        time.sleep(1)

if __name__ == "__main__":
    main()
```

**Subscriber (subscriber.py):**

```python
import zmq

def main():
    context = zmq.Context()

    # Create a SUB socket to receive messages from the forwarder
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5556")
    socket.setsockopt_string(zmq.SUBSCRIBE, "")

    while True:
        # Wait for a message from the forwarder
        message = socket.recv()
        print(f"Subscriber received message: {message}")

if __name__ == "__main__":
    main()
```

---

---

---

### 3. `Streamer` for (`Clients` and `Workers`)

A `Streamer` device forwards messages between a PULL socket and a PUSH socket, typically used for task distribution patterns.

**Streamer (streamer.py):**

```python
import zmq
from zmq.devices import ProcessDevice

def main():
    # Create a ProcessDevice for STREAMER
    streamer_device = ProcessDevice(zmq.STREAMER, zmq.PULL, zmq.PUSH)

    # Bind the frontend socket to receive messages from clients
    streamer_device.bind_in("tcp://*:5555")

    # Bind the backend socket to send tasks to workers
    streamer_device.bind_out("tcp://*:5556")

    # Start the device
    streamer_device.start()

    print("Streamer started, waiting for clients and workers...")

if __name__ == "__main__":
    main()
```

**Client (client.py):**

```python
import zmq

def main():
    context = zmq.Context()

    # Create a PUSH socket to send tasks to the streamer
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://localhost:5555")

    # Send a task to the streamer
    task = b"Task"
    print(f"Client sending task: {task}")
    socket.send(task)

if __name__ == "__main__":
    main()
```

**Worker (worker.py):**

```python
import zmq

def main():
    context = zmq.Context()

    # Create a PULL socket to receive tasks from the streamer
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://localhost:5556")

    while True:
        # Wait for a task from the streamer
        task = socket.recv()
        print(f"Worker received task: {task}")

if __name__ == "__main__":
    main()
```

---

---

---

### Summary

These examples illustrate how to use `zmq.devices.ProcessDevice` to set up different types of ZeroMQ devices:

- **Queue** for request-response patterns.
- **Forwarder** for publish-subscribe patterns.
- **Streamer** for task distribution patterns.

Each example includes the necessary code for the broker, client, and worker or subscriber components.
