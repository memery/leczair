import random, string

from logging import getLogger

import state

from .parser import Message, parse_privmsg, get_nick
from .render import to_raw


logger = getLogger(__name__)


def init(sock, state):
    irc_settings = state.settings.irc
    send_message(sock, Message(command='NICK', arguments=[irc_settings.nick]))

    user_arguments = [irc_settings.nick, '0', '*',
                     'IRC bot {}'.format(irc_settings.nick)]
    send_message(sock, Message(command='USER', arguments=user_arguments))

    state.irc.nick = irc_settings.nick
    state.irc.joined = False
    state.irc.registered = False


def manage(message, state):
    if message.command == 'PING':
        return Message(command='PONG', arguments=message.arguments)
    elif message.command == '403':
        # Channel doesn't exist, stop trying to join
        state.settings.irc.channel = None
    elif message.command == '433':
        def new_nick_proposal(nick):
            # determine how much to shave off to make room for random chars
            nick = nick[:min(len(nick), 6)]

            random_choices = string.ascii_lowercase + string.digits
            random_chars = ''.join(random.choice(random_choices)
                                   for x in range(2))

            return '{}_{}'.format(nick, random_chars)

        nick = state.settings.irc.nick

        logger.warning('Nick %s is already in use', nick)

        new_nick = new_nick_proposal(nick)
        state.irc.nick = new_nick

        return Message(command='NICK', arguments=[new_nick])
    elif message.command == '001':
        state.irc.nick = message.arguments[0]
        state.irc.registered = True
    elif message.command == 'JOIN' and get_nick(message) == state.irc.nick:
        state.irc.joined = True


def get_message(sock, state):
    raw_message = sock.read()
    if not raw_message:
        if state.settings.irc.channel and not state.irc.joined \
           and state.irc.registered:
            send_message(sock, Message(command='JOIN',
                                       arguments=[state.settings.irc.channel]))
        return None

    message = Message(raw_message=raw_message)

    response = manage(message, state)
    if response:
        send_message(sock, response)
        return None

    if message.command == 'PRIVMSG':
        return parse_privmsg(message)
    else:
        return None


def send_message(sock, message):
    sock.write(to_raw(message))
