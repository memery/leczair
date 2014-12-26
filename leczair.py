import json
import logging

import importlib
from contextlib import contextmanager
from time import sleep

from stateobj import State, from_dict

import irc
import network
import behaviour


NETWORK_EXCEPTIONS = (BrokenPipeError, ConnectionResetError,
                      ConnectionAbortedError, ConnectionRefusedError)


logger = logging.getLogger(__name__)


def load_settings():
    with open('settings.json', 'r') as conf:
        return from_dict(json.load(conf))


def reload_modules(modules=frozenset({irc, network, behaviour})):
    reloaded = set()
    for m in modules:
        try:
            importlib.reload(m)
        except Exception as e:
            logger.exception(e)
        else:
            reloaded.add(m.__name__)

    logger.info('Reloaded {}'.format(', '.join(reloaded)))


def run_bot(state):
    try:
        state.network = network.init(state.settings.irc)
        irc.hello(state.network, state.settings.irc, state.irc)

        while True:
            try:
                message = irc.get_message(state.network, state.settings.irc, state.irc)
                state.behaviour.nick = state.irc.nick

                if message:
                    # TODO: Temporary until we know more about how admin
                    # commands are going to work
                    if message.text == 'reload':
                        reload_modules()
                        continue
                    if message.text == 'restart':
                        return 'restart'

                    response = behaviour.handle(message, state.behaviour)
                    if response:
                        irc.send_message(state.network, response)

            except (BrokenPipeError, ConnectionResetError,
                    ConnectionAbortedError, ConnectionRefusedError):
                raise
            except Exception as e:
                logger.exception(e)

    except Exception as e:
        # Gotta catch 'em all because if we don't catch it by now, fire and
        # explosions will ensue
        logger.exception(e)

        # If anything is thrown and caught here, there's no point in trying to
        # do anything about it because we've already exited the connection
        # maintenance loop, so we just wait a bit and try to reconnect again.
        sleep(30)
    finally:
        network.close(state.network)
        # Clear the IRC connection specific state when the connection as been
        # killed
        state.irc = State()

