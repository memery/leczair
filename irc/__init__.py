
from irc.parser import Message, parse_privmsg

def init(sock, state):
    irc_settings = state.settings.irc
    send_message(sock, Message(command='NICK', arguments=[irc_settings.nick]))
    send_message(sock, Message(command='USER', arguments=[irc_settings.nick, '0', '*', 'IRC bot {}'.format(irc_settings.nick)]))
    state.irc.joined = False


def manage(raw_msg, state):
    if message.command == 'PING':
        return Message(command='PONG', arguments=message.arguments)
    elif message.command == '403':
        # Channel doesn't exist, stop trying to join
        state.settings.irc.channel = None


def get_message(sock, state):
    raw_message = sock.read()
    if not raw_message:
        return None

    response = manage(raw_message, state)
    if response:
        send_message(sock, response)
        return None

    return parse_privmsg(message)


def send_message(sock, msg):
    # socket.send(to_raw_message(internal_message))
    pass

