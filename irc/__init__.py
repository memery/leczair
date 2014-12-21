import state

from .parser import Message, parse_privmsg, get_nick
from .render import to_raw


def init(sock, state):
    irc_settings = state.settings.irc
    send_message(sock, Message(command='NICK', arguments=[irc_settings.nick]))
    send_message(sock, Message(command='USER', arguments=[irc_settings.nick, '0', '*', 'IRC bot {}'.format(irc_settings.nick)]))
    state.irc.nick = irc_settings.nick
    state.irc.joined = False


def manage(message, state):
    if message.command == 'PING':
        return Message(command='PONG', arguments=message.arguments)
    elif message.command == '403':
        # Channel doesn't exist, stop trying to join
        state.settings.irc.channel = None
    elif message.command == 'JOIN' and get_nick(message) == state.irc.nick:
        state.irc.joined = True


def get_message(sock, state):
    raw_message = sock.read()
    if not raw_message:
        if state.settings.irc.channel and not state.irc.joined:
            send_message(sock, Message(command='JOIN', arguments=[state.settings.irc.channel]))
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
