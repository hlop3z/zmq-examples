# Python
from collections import namedtuple
from contextlib import contextmanager
from functools import partial
from types import SimpleNamespace
from typing import Literal, Any
import dataclasses as dc
import logging

# ZMQ
import zmq
import zmq.asyncio
from zmq.devices import ProcessDevice as Device

# https://pyzmq.readthedocs.io/en/latest/howto/ssh.html
from zmq.ssh.tunnel import tunnel_connection

Mesh = namedtuple("Mesh", ["device", "backend", "frontend"], module="ZeroMQ")


def tcp_string(port: int = 5555, host: str = "127.0.0.1"):
    """
    Generates a TCP Address.

    Args:
        port (int): The port number.
        host (str): The host address.

    Returns:
        str: The TCP address for the local host with the specified port.
    """
    return f"tcp://{host}:{port}"


def zmq_context(is_sync: bool = False):
    """
    Get ZMQ `Context`.
    """
    if is_sync:
        context = zmq.Context.instance()
    else:
        context = zmq.asyncio.Context()  # type: ignore
    return context


def network_types(type_name: str = "queue"):
    """
    Get **ZMQ Types** for `Device` and `Socket`.

    Options:
        - `queue`       for (`Request` and `Response`)
        - `forwarder`   for (`Publisher` and `Subscriber`)
        - `streamer`    for (`Clients` and `Workers`)
    """
    match type_name.lower():
        case "queue":
            return Mesh(
                device=Device(zmq.QUEUE, zmq.ROUTER, zmq.DEALER),
                backend=zmq.REP,
                frontend=zmq.REQ,
            )
        case "forwarder":
            return Mesh(
                device=Device(zmq.FORWARDER, zmq.SUB, zmq.PUB),
                backend=zmq.SUB,
                frontend=zmq.PUB,
            )
        case "streamer":
            return Mesh(
                device=Device(zmq.STREAMER, zmq.PULL, zmq.PUSH),
                backend=zmq.PULL,
                frontend=zmq.PUSH,
            )


class ZeroMQ:
    """ZeroMQ Manager"""

    tcp = tcp_string

    def __init__(
        self,
        mode: Literal["device", "backend", "frontend"] = "device",
        backend: str = tcp_string(5556),  # inproc://workers
        frontend: str = tcp_string(5555),  # inproc://clients
        timeout: int = 5000,
        is_sync: bool = False,
        network_type: str = "queue",
        ssh: "SSH" | None = None,
    ) -> "ZeroMQ":
        """
        Initialize a ZeroMQ.
        """
        # Mode
        self.mode = mode

        # Options
        self.timeout = timeout
        self.ssh = ssh

        # URL(s)
        self.url = self.__get_urls(backend, frontend)

        # ZMQ
        self.socket = None
        self.mesh = network_types(network_type)
        self.context = zmq_context(is_sync)
        self.get_context = partial(zmq_context, is_sync)

    def __get_urls(self, backend, frontend):
        """
        Get URL(s)
        """
        match self.mode:
            case "device":
                return SimpleNamespace(backend=backend, frontend=frontend)
            case "backend":
                return SimpleNamespace(backend=backend, frontend=None)
            case "frontend":
                return SimpleNamespace(backend=None, frontend=frontend)

    def device(self):
        """
        Start the ZMQ `Device`.
        """
        proxy = self.mesh.device
        proxy.bind_in(self.url.frontend)
        proxy.bind_out(self.url.backend)
        proxy.start()
        logging.info("Starting Broker Device...")

    def backend(self):
        """
        Start the ZMQ backend `Server`.
        """
        self.socket = self.context.socket(self.mesh.backend)
        self.socket.bind(self.url.backend)

    def frontend(self):
        """
        Start the ZMQ frontend `Client`.
        """
        self.socket = self.context.socket(self.mesh.frontend)

    def __connect(
        self, socket: Any, send_timeout: bool | int, receive_timeout: bool | int
    ):
        """
        Connection to the ZMQ socket.
        """
        if False:
            tunnel_connection(
                socket,
                self.url.frontend,  # "tcp://locahost:5555"
                self.ssh_host,  # "myuser@remote-server-ip"
                keyfile=self.ssh_keyfile,
            )
        else:
            socket.connect(self.url.frontend)
        # Timeouts
        if send_timeout:
            socket.setsockopt(
                zmq.SNDTIMEO, self.timeout if send_timeout is True else send_timeout
            )
        if receive_timeout:
            socket.setsockopt(
                zmq.RCVTIMEO,
                self.timeout if receive_timeout is True else receive_timeout,
            )

    @contextmanager
    def connect(
        self, send_timeout: bool | int = True, receive_timeout: bool | int = True
    ):
        """
        Establishes a `connection` to the ZMQ socket.
        """
        # Context & Socket
        context: Any = self.get_context()
        c_socket: Any = context.socket(zmq.REQ)
        # Request
        try:
            self.__connect(c_socket, send_timeout, receive_timeout)
            yield c_socket
        except zmq.Again as e:
            logging.error(e)
            c_socket.setsockopt(zmq.LINGER, 0)
            c_socket.close()
        finally:
            c_socket.close()
            context.term()


@dc.dataclass
class SSH:
    server: Any
    keyfile: Any | None = None
    password: Any | None = None
    paramiko: Any | None = None
    timeout: int = 60
