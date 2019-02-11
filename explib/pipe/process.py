"""Pipe implementation for processes."""

import os
import select
import subprocess

from explib.pipe.pipe import Pipe


__all__ = ['Process']


class Process(Pipe):
    """Pipe implementation for processes."""

    def __init__(self, argv, env=None, timeout=0.1):
        super().__init__(timeout)

        self.proc = subprocess.Popen(argv,
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT,
                                     env=env)

    def recv(self, bufsize):
        rlist, _, _ = select.select([self.proc.stdout], [], [], self.timeout)
        if rlist:
            return os.read(self.proc.stdout.fileno(), bufsize)
        else:
            raise TimeoutError

    def send(self, data):
        _, wlist, _ = select.select([], [self.proc.stdin], [], self.timeout)
        if wlist:
            return os.write(self.proc.stdin.fileno(), data)
        else:
            raise TimeoutError

    def close(self):
        for procfile in [self.proc.stdin, self.proc.stdout, self.proc.stderr]:
            if procfile:
                procfile.close()

        try:
            self.proc.kill()
            self.proc.wait()
        except OSError:
            pass

    def pid(self):
        """Returns the PID of the process."""
        return self.proc.pid
