
"""
A module with some convenience functions to create IRC messages.

"""

from .serialisation import Message

def privmsg(recipient, text):
    return Message(command='PRIVMSG', arguments=[recipient, text])

def join(channel):
    return Message(command='JOIN', arguments=[channel])

def part(channel):
    return Message(command='PART', arguments=[channel])

def nick(new_nick):
    return Message(command='NICK', arguments=[new_nick])

def user(user_name, real_name):
    return Message(command='USER', arguments=[user_name, '0', '*', real_name])

def pong(*args):
    return Message(command='PONG', arguments=args)

