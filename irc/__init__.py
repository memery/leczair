import random, string
from logging import getLogger
from extrafunctools import identity
import network
from message import Message
import frozenstate
from .serialisation import from_raw, to_raw


logger = getLogger(__name__)


def settings_changed(old_settings, new_settings):
    
    """
    What do we need to take care of when settings are reloaded?

    """

    yield Message.nick(new_settings.nick)


def hello(sock, settings, state):
    
    """
    Sends the basic identy information to the IRC server and sets some
    initial state required by the rest of the irc module procedures.

    """

    send_message(sock, Message.nick(settings.nick))
    send_message(sock, Message.user(settings.nick,
                                    'Bot {}'.format(settings.nick)))

    return frozenstate.from_dict({
        'nick': settings.nick,
        'joined': '',
    })


def manage(message, settings, state):

    """
    Takes a message and determines if it requires some administrative
    connection management, such as responding to a PING, or changing
    nicks, or joining channels or whatever. Returns a message to be
    sent to the server with the action taken. If None is returned, no
    action needs to be taken by the server.

    """

    if message.command == 'PING':
        return Message.pong(*message.arguments), frozenstate.empty()
    elif message.command == '403':
        # Channel doesn't exist, stop trying to join
        # TODO: fix :( settings.channel = None
        return None, frozenset.empty()
    elif message.command == '433':
        def generate_nick(nick):
            truncated = nick[:min(len(nick), 6)]
            alphabet = string.ascii_lowercase + string.digits
            random_chars = ''.join(random.choice(alphabet) for _ in range(2))
            return '{}_{}'.format(truncated, random_chars)

        logger.warning('Nick %s is already in use', state.nick)

        new_nick = generate_nick(settings.nick)
        return Message.nick(new_nick), frozenstate.single('nick', new_nick)
    elif message.command == '001':
        return None, frozenstate.single('nick', message.arguments[0])
    elif message.command == 'JOIN':
        if getattr(message, 'origin', None) == state.nick:
            return None, frozenstate.single('joined', message.arguments[0])
    else:
        return None, frozenstate.empty()


def get_message(sock, settings, state):

    """
    Read a message from the IRC connection, simulaneously making sure
    to keep the connection alive and handling the IRC statey business.
    Returns the message, perhaps with convenience information attached.

    """

    raw_message = network.read(sock)

    if raw_message:
        message = from_raw(raw_message)
        response, new_state = manage(message, settings, state)
        if response:
            send_message(sock, response)
        elif message.command == 'PRIVMSG':
            return message, new_state

        return None, new_state

    if settings.channel != state.joined:
        if state.joined:
            send_message(sock, Message.part(state.joined))
        send_message(sock, Message.join(settings.channel))
        return None, frozenstate.empty()



def send_message(sock, message):
    network.write(sock, to_raw(message))

