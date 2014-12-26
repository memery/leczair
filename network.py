import socket

from ssl import wrap_socket
from logging import getLogger
from contextlib import suppress


logger = getLogger(__name__)


class BufferedSocket:

    """
    A buffered SSL agnostic socket object. The read method will
    either return a complete received line (without crlf) or, if
    no such line exists, try to get more data from the backing
    socket and then return None.

    """

    def __init__(self, connection):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((connection.host, connection.port))

        self.sock.settimeout(1)

        if connection.ssl:
            self.sock = wrap_socket(self.sock)

        self.ssl = connection.ssl
        self.buffer = b''


    def read(self):

        """
        Tries to return a line from the buffer. If none exists,
        it reads in one more to the buffer and returns None.

        """

        try:
            byteline, self.buffer = self.buffer.split(b'\r\n', 1)
            read_data = byteline.decode('utf-8')

            logger.debug('Read: %s', read_data)

            return read_data
        except ValueError:
            more = self.sock.read if self.ssl else self.sock.recv
            with suppress(socket.timeout):
                self.buffer += more(4096)

            return None


    def write(self, text):

        """
        Accepts a a string object as text, encodes it as utf-8 and
        puts it out to the socket.

        """

        logger.debug('Wrote: %s', text)

        self.sock.send(bytes(text + '\n', 'utf-8'))


    def close(self):
        self.sock.close()
