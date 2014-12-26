import re
import logging

from importlib import import_module, reload

from irc import Message


logger = logging.getLogger(__name__)


def response(recipient, text):
    return Message(command='PRIVMSG', arguments=[recipient, text])


def run_plugins(message, plugins):
    logger.debug('Run plugins')
    return (reload(import_module('plugins.' + plugin)).run(message)
            for plugin in plugins)


def handle(message, state, settings):
    try:
        to, text = split_text(message.text)
    except TypeError:
        pass
    else:
        if to == state.nick and text == 'hello':
            yield response(message.recipient, 
                           'hello to you too, {}!'.format(message.origin))

    yield from run_plugins(message, settings.plugins)


def split_text(text):
    m = re.fullmatch(r'([^ ]+?).? (.+)', text)
    return m.group(1, 2) if m else None
