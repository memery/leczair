import json, logging

from state import State, from_dict
import irc, network


logger = logging.getLogger(__name__)


def log_exceptions(f):
    def new_f(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                logger.error(e)

    return new_f


def load_settings():
    with open('settings.json', 'r') as conf:
        return from_dict(json.load(conf))


@log_exceptions
def init():
    state = State()
    state.settings = load_settings()
    sock = network.BufferedSocket(state.settings.irc.host,
                                  state.settings.irc.port,
                                  ssl=state.settings.irc.ssl)

    irc.init(sock, state)

    return sock, state


@log_exceptions
def main_loop(sock, state):
    while True:
        irc.get_message(sock, state)


if __name__ == '__main__':
    # set up logging
    logging.basicConfig(level=logging.DEBUG)

    sock, state = init()
    main_loop(sock, state)


