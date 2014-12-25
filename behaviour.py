
import re
from irc import Message


def response(recipient, text):
    return Message(command='PRIVMSG', arguments=[recipient, text])


def handle(message, state):
    try:
        to, text = split_text(message.text)
    except TypeError:
        return None
    else:
        if to == state.nick and text == 'hello':
            return response(message.recipient, 
                'hello to you too, {}!'.format(message.origin) 
            )


def split_text(text):
    m = re.fullmatch(r'([^ ]+?).? (.+)', text)
    return m.group(1, 2) if m else None


