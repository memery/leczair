from irc import Message
from extrafunctools import modattr, succ


def run(message, state):
    if message.text.endswith('++'):
        thing = message.text.rstrip('+')
        if thing in state:
            modattr(state, thing, succ)
        else:
            setattr(state, thing, 1)

        return Message(command='PRIVMSG',
                       arguments=[message.recipient,
                                  '{} = {}'.format(thing,
                                                   getattr(state, thing))])
