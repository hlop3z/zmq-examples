import zmq


def main(shutdown_event):
    context = zmq.Context()

    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt(zmq.SUBSCRIBE, b"status")

    while not shutdown_event.is_set():
        message = socket.recv_multipart()
        print(f"Received: {message}")
