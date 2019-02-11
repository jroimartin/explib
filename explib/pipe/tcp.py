"""Pipe implementation for TCP connections."""

import socket

from explib.pipe.pipe import Pipe


__all__ = ['TCPSocket']


class TCPSocket(Pipe):
    """Pipe implementation for TCP connections."""

    def __init__(self, host, port, timeout=0.1):
        super().__init__(timeout)

        self.sock = socket.create_connection((host, port), timeout)

    def settimeout(self, timeout):
        super().settimeout(timeout)

        self.sock.settimeout(timeout)

    def recv(self, bufsize):
        try:
            return self.sock.recv(bufsize)
        except socket.timeout:
            raise TimeoutError

    def send(self, data):
        try:
            return self.sock.send(data)
        except socket.timeout:
            raise TimeoutError

    def close(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
