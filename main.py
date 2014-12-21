import json, logging

from state import State, from_dict
import irc, network



def load_settings():
    with open('settings.json', 'r') as conf:
        return from_dict(json.load(conf))


def init():
    state = State()
    state.settings = load_settings()
    sock = network.BufferedSocket(state.settings.irc.host,
                                  state.settings.irc.port,
                                  ssl=state.settings.irc.ssl)

    # set up logging
    logging.basicConfig(level=logging.DEBUG)

    irc.init(sock, state)
    while True:
        irc.get_message(sock, state)


if __name__ == '__main__':
    init()


