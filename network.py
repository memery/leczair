
"""
A buffered SSL agnostic socket module. The read procedure will
either return a complete received line (without CRLF) or, if
no such line exists, try to get more data from the backing
socket and then return None.

"""


import socket

from ssl import wrap_socket
from logging import getLogger
from contextlib import suppress
import frozenstate

logger = getLogger(__name__)


def init(connection):

    """
    Sets up the necessary state information to be able to use the
    read/write procedures. Returns the state object the other methods
    expect

    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((connection.host, connection.port))
    sock.settimeout(1)

    if connection.ssl:
        sock = wrap_socket(sock)

    return frozenstate.from_dict({
        'sock': sock,
        'ssl': connection.ssl,
        'buffer': b'',
    })


def read(state):

    """
    Tries to return a line from the buffer. If none exists,
    it reads in one more to the buffer and returns None.

    """

    try:
        byteline, new_buffer = state.buffer.split(b'\r\n', 1)
        read_data = byteline.decode('utf-8')

        logger.debug('--> %s', read_data)
    except ValueError:
        read_data = None

        more = state.sock.read if state.ssl else state.sock.recv
        with suppress(socket.timeout):
            new_buffer = state.buffer + more(4096)

    return read_data, frozenstate.single('buffer', new_buffer)


def write(state, text):

    """
    Accepts a a string object as text, encodes it as utf-8 and
    puts it out to the socket.

    """

    logger.debug('<-- %s', text)
    state.sock.send(bytes(text + '\n', 'utf-8'))


def close(state):
    state.sock.close()
