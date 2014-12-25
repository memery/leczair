import json
import logging

import traceback
from contextlib import contextmanager
from time import sleep

from state import State, from_dict

import irc
import network


logger = logging.getLogger(__name__)


class LoggerFileWrapper:
    def __init__(self, logging_fn):
        self.logging_fn = logging_fn

    def write(self, string):
        for line in string.splitlines():
            if line:
                self.logging_fn(line)


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

            irc.get_message(sock, state.settings.irc, state.irc)
        except (BrokenPipeError, ConnectionResetError) as e:
            socket = None
            sleep(30)
        except (ConnectionAbortedError, ConnectionRefusedError) as e:
            logger.error('Connection refused by the server, quitting...')
            return
        except Exception as e:
            traceback.print_exc(3, LoggerFileWrapper(logger.error))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    state = State()
    state.settings = load_settings()
    run_bot(state)

