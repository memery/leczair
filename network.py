import socket
from ssl import wrap_socket


class BufferedSocket(object):

    """
    bufsock

    """

    def __init__(self, host, port, ssl=False, sock=None):
        if not sock:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))

            sock.settimeout(1)

        if ssl:
            sock = wrap_socket(sock)

        self.sock = sock

        self.ssl = ssl
        self.buffer = b''

    def read(self):

        """
        Tries to return a line from the buffer. If none exists, it reads in
        ome more to the buffer and returns None.

        """

        try:
            byteline, self.buffer = self.buffer.split(b'\r\n', 1)
            return byteline.decode('utf-8')
        except ValueError:
            with ignored(socket.timeout):
                self.buffer += (self.sock.read(4096)
                                if self.ssl else self.sock.recv(4096))

    def write(self, text):

        """
        Accepts a a string object as text, encodes it as utf-8 and  puts it
        out to the socket.

        """

        self.sock.send(bytes(text + '\n', 'utf-8'))
