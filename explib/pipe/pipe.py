"""
Pipe module.

Pipes provide an abstraction layer on top of sockets, processes,
debugged processes, etc.
"""

import re
from contextlib import contextmanager


class Pipe:
    """Base class for Pipe implementations."""

    def __init__(self, timeout):
        self.timeout = timeout

    def settimeout(self, timeout):
        """Set IO timeout."""
        self.timeout = timeout

    def gettimeout(self):
        """Get current timeout."""
        return self.timeout

    @contextmanager
    def _tmp_timeout(self, timeout):
        """Set up a context with a temporary timeout."""
        try:
            if timeout:
                old_timeout = self.gettimeout()
                self.settimeout(timeout)
            yield
        finally:
            if timeout:
                self.settimeout(old_timeout)

    def recv(self, bufsize):
        """Receive up to buffersize bytes from the pipe."""
        raise NotImplementedError

    def send(self, data):
        """
        Send data to the pipe.

        Return the number of bytes sent, this may be less than len(data).
        """
        raise NotImplementedError

    def close(self):
        """Close the pipe. It cannot be used after this call."""
        raise NotImplementedError

    def _read_regex(self, pattern, bufsize=4096, timeout=None):
        """
        Read data from pipe until the given regex pattern matches.

        Return received data and a match object.
        """
        cre = re.compile(pattern, re.MULTILINE | re.DOTALL)

        buf = b''

        with self._tmp_timeout(timeout):
            while True:
                ret = self.recv(bufsize)
                if not ret:  # EOF
                    raise EOFError

                buf += ret

                match = cre.search(buf)
                if match:
                    break

        return buf, match

    def read_until(self, pattern, bufsize=4096, timeout=None):
        """
        Read data from pipe until the given regex pattern matches.

        Return received data.
        """
        buf, _match = self._read_regex(pattern, bufsize, timeout)
        return buf

    def read_search(self, pattern, bufsize=4096, timeout=None):
        """
        Read data from pipe until the given regex pattern matches.

        Return a match object.
        """
        _buf, match = self._read_regex(pattern, bufsize, timeout)
        return match

    def readall(self, bufsize=4096, timeout=None):
        """Read remaining data from pipe."""
        buf = b''

        with self._tmp_timeout(timeout):
            while True:
                try:
                    ret = self.recv(bufsize)
                    if not ret:  # EOF
                        break

                    buf += ret
                except TimeoutError:
                    break

        return buf

    def sendall(self, data):
        """Send all data to the pipe."""
        ret = 0
        while ret < len(data):
            ret += self.send(data[ret:])

    def interact(self):
        """Starts an interactive client."""
        while True:
            cmd = input('> ') + '\n'
            self.sendall(cmd.encode('utf-8'))
            ret = self.readall().decode('utf-8')
            print(ret)
