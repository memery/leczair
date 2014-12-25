import json
import logging

from time import sleep

from state import State, from_dict

import irc
import network
import behaviour


logger = logging.getLogger(__name__)


def load_settings():
    with open('settings.json', 'r') as conf:
        return from_dict(json.load(conf))


def run_bot(state):
    sock = None

    while True:
        try:
            if not sock:
                sock = network.BufferedSocket(state.settings.irc)
                irc.hello(sock, state.settings.irc, state.irc)

            message = irc.get_message(sock, state.settings.irc, state.irc)
            state.behaviour.nick = state.irc.nick

            if message:
                response = behaviour.handle(message, state.behaviour)
                if response:
                    irc.send_message(sock, response)


        except (BrokenPipeError, ConnectionResetError) as e:
            socket = None
            sleep(30)
        except (ConnectionAbortedError, ConnectionRefusedError) as e:
            logger.error('Connection refused by the server, quitting...')
            return
        except Exception as e:
            logger.exception(e)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    state = State()
    state.settings = load_settings()
    run_bot(state)

