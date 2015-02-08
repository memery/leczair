import json
import logging
import re

import importlib
from contextlib import contextmanager
from time import sleep

import frozenstate

import irc
import network
import message
import behaviour
import extrafunctools


logger = logging.getLogger(__name__)


def load_settings():
    with open('settings.json', 'r') as conf:
        return frozenstate.from_dict(json.load(conf))


def reload_modules(modules=frozenset({irc, network, message, behaviour, extrafunctools})):
    reloaded = set()
    for m in modules:
        try:
            importlib.reload(m)
        except Exception as e:
            logger.exception(e)
        else:
            reloaded.add(m.__name__)

    logger.info('Reloaded {}'.format(', '.join(reloaded)))


def is_admin(settings, user):
    return any(re.fullmatch(admin, user) for admin in settings.admins)


def run_bot(state):
    try:
        connection = network.init(state.settings.irc)
        # TODO: Fix so this uses the auto state creating thingey
        state = frozenstate.append(state,
                irc.hello(connection, state.settings.irc, getattr(state, 'irc', frozenstate.empty())))

        while True:
            try:
                message = irc.get_message(connection, state.settings.irc, state.irc)
                state.behaviour.nick = state.irc.nick

                if message:
                    # TODO: Temporary until we know more about how admin
                    # commands are going to work
                    if is_admin(state.settings, message.user):
                        if message.text == 'reconfigure':
                            old = state.settings
                            state = frozenstate.append(state, load_settings())
                            msgs = irc.settings_changed(old.irc,
                                                        state.settings.irc)
                            for msg in msgs:
                                irc.send_message(connection, msg)
                        if message.text == 'reload':
                            reload_modules()
                            continue
                        if message.text == 'restart':
                            return 'restart'

                    responses = behaviour.handle(message, state.settings,
                                                 state.behaviour)

                    for response in filter(bool, responses):
                        irc.send_message(connection, response)

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
        network.close(active_network)
        # Clear the IRC connection specific state when the connection as been
        # killed
        state.irc = frozenstate.empty()

