import re
import logging

from importlib import import_module, reload
from itertools import chain

from classes import Message


logger = logging.getLogger(__name__)


def run_plugins(message, command_prefix, plugins, state):
    logger.debug('Run plugins')
    return chain.from_iterable(
        reload(
            import_module('plugins.' + plugin)
        ).run(
            message,
            command_prefix,
            getattr(state, plugin)
        ) or () # default to empty iterable
        for plugin in plugins
    )


def handle(message, settings, state):
    try:
        to, text = split_text(message.text)
    except TypeError:
        pass
    else:
        if to == state.nick and text == 'hello':
            yield Message.privmsg(message.recipient, 
                'hello to you too, {}!'.format(message.origin))

    yield from run_plugins(message, settings.behaviour.command_prefix,
                           settings.plugins, state.plugins)


def split_text(text):
    m = re.fullmatch(r'([^ ]+?).? (.+)', text)
    return m.group(1, 2) if m else None
