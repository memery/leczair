import random, string
from logging import getLogger
from underscore import id
import network
from .parser import Message, parse_privmsg, get_nick
from .render import to_raw


logger = getLogger(__name__)


def create_socket(irc):
    return network.BufferedSocket(irc.host, irc.port, ssl=irc.ssl)


def hello(sock, settings, state):
    
    """
    Sends the basic identy information to the IRC server and sets some
    initial state required by the rest of the irc module procedures.

    """

    send_message(sock, Message(command='NICK', arguments=[settings.nick]))

    user_arguments = [settings.nick, '0', '*', 'Bot {}'.format(settings.nick)]
    send_message(sock, Message(command='USER', arguments=user_arguments))

    state.nick = settings.nick
    state.joined = ''


def manage(message, settings, state):

    """
    Takes a message and determines if it requires some administrative
    connection management, such as responding to a PING, or changing
    nicks, or joining channels or whatever. Returns a message to be
    sent to the server with the action taken. If None is returned, no
    action needs to be taken by the server.

    """

    if message.command == 'PING':
        return Message(command='PONG', arguments=message.arguments)
    elif message.command == '403':
        # Channel doesn't exist, stop trying to join
        settings.channel = None
    elif message.command == '433':
        def generate_nick(nick):
            truncated = nick[:min(len(nick), 6)]
            alphabet = string.ascii_lowercase + string.digits
            random_chars = ''.join(random.choice(alphabet) for _ in range(2))
            return '{}_{}'.format(truncated, random_chars)

        logger.warning('Nick %s is already in use', state.nick)

        state.nick = generate_nick(settings.nick)
        return Message(command='NICK', arguments=[state.nick])
    elif message.command == '001':
        state.nick = message.arguments[0]
    elif message.command == 'JOIN' and get_nick(message) == state.nick:
        state.joined = message.arguments[0]


def get_message(sock, settings, state):

    """
    Read a message from the IRC connection, simulaneously making sure
    to keep the connection alive and handling the IRC statey business.
    Returns the message, perhaps with convenience information attached.

    """

    raw_message = sock.read()
    if not raw_message:
        if settings.channel != state.joined:
            send_message(sock, Message(command='JOIN',
                                       arguments=[settings.channel]))
        return None

    message = Message(raw_message=raw_message)

    response = manage(message, settings, state)
    if response:
        send_message(sock, response)
        return None

    amend = parse_privmsg if message.command == 'PRIVMSG' else id
    return amend(message)


def send_message(sock, message):
    sock.write(to_raw(message))
