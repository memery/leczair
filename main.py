import json, logging
from contextlib import contextmanager

from state import State, from_dict
import irc, network


logger = logging.getLogger(__name__)


@contextmanager
def log_exceptions():
    try:
        yield
    except Exception as e:
        # TODO: Make new logger so that the right module name is used.
        logger.error(e)


def load_settings():
    with open('settings.json', 'r') as conf:
        return from_dict(json.load(conf))


def init():
    # set up logging
    logging.basicConfig(level=logging.DEBUG)

    with log_exceptions():
        state = State()
        state.settings = load_settings()
        sock = network.BufferedSocket(state.settings.irc.host,
                                      state.settings.irc.port,
                                      ssl=state.settings.irc.ssl)

        irc.init(sock, state)

        while True:
            with log_exceptions():
                irc.get_message(sock, state)


if __name__ == '__main__':
    init()
