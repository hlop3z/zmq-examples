import time
import zmq


# signal.signal(signal.SIGINT, signal.SIG_DFL)


def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    time.sleep(1)
    socket.send(b"status 5")
    socket.send(b"All is well")
