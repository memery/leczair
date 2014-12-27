from irc import privmsg
from extrafunctools import modattr, succ


def run(message, state):
    if message.text.endswith('++'):
        thing = message.text.rstrip('+')
        if thing in state:
            modattr(state, thing, succ)
        else:
            setattr(state, thing, 1)

        response = 'The value of {} is now {}'.format(thing, getattr(state, thing))
        return privmsg(message.recipient, response)
