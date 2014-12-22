import json
import logging

from contextlib import contextmanager

from state import State, from_dict, to_dict

import irc
import network


logger = logging.getLogger(__name__)


@contextmanager
def log_exceptions():
    try:
        yield
    except Exception as e:
        # TODO: Make new logger so that the right module name is used.
        logger.error(e)


@contextmanager
def maintain_connection(state):
    class SocketNotCreatedError(Exception):
        pass

    try:
        if not state.sock:
            raise SocketNotCreatedError

        yield state.sock
    except (BrokenPipeError, ConnectionResetError, SocketNotCreatedError):
        state.sock = create_irc_socket(state)
        irc.init(state.sock, state)
        yield state.sock


def load_settings():
    with open('settings.json', 'r') as conf:
        return from_dict(json.load(conf))


def create_irc_socket(state):
    args = [state.settings.irc.host, state.settings.irc.port]
    kwargs = {'ssl': state.settings.irc.ssl}
    return network.BufferedSocket(*args, **kwargs)


def init():
    # set up logging
    logging.basicConfig(level=logging.DEBUG)

    state = State()
    state.settings = load_settings()
    state.sock = None

    while True:
        with log_exceptions(), maintain_connection(state) as sock:
            irc.get_message(sock, state)


if __name__ == '__main__':
    init()
