
import socket

def make_socket(host, port, ssl=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    if ssl:
        sock = ssl_wrap(socket)

    sock.settimeout(1)

    return BufferedSocket(sock, ssl)


class BufferedSocket(object):
    """bufsock"""

    def __init__(self, sock, ssl):
        self.sock = sock
        self.ssl = ssl
        self.buffer = b''

    def read(self):
        """Tries to return a line from the buffer. If none exists, it
           reads in some more to the buffer and returns None."""
        try:
            byteline, self.buffer = self.buffer.split(b'\r\n', 1)
            return byteline.decode('utf-8')
        except ValueError:
            with ignored(socket.timeout):
                self.buffer += self.sock.read(4096) if self.ssl else self.sock.recv(4096)


    def write(self, text):
        """Accepts a a string object as text, encodes it as utf-8 and
           puts it out to the socket."""
        self.sock.send(bytes(text + '\n', 'utf-8'))

