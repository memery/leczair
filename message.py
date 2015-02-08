import re

class Message:

    """
    An internal message data structure, with fields such as msg.user,
    msg.command and so on.

    """

    def __init__(self, command, arguments=None):
        arguments = list(arguments) if arguments else []
        for section in arguments + [command]:
            if any(map(lambda s: ord(s) < 32, section)):
                raise ValueError('The message contains ASCII control characters:: {}'.format(repr(section)))
        self.command = command
        self.arguments = arguments

    @property
    def text(self):
        if self.command == 'PRIVMSG':
            return self.arguments[1]
        else:
            raise AttributeError('message type {} does not have text'.format(self.command))

    @property
    def recipient(self):
        if self.command == 'PRIVMSG':
            return self.arguments[0]
        else:
            raise AttributeError('message type {} does not have a recipient'.format(self.command))

    @property
    def origin(self):
        return re.match(r'~?([^!]+)!', self.user).group(1)

    @classmethod
    def privmsg(cls, recipient, text):
        return cls('PRIVMSG', arguments=[recipient, text])

    @classmethod
    def join(cls, channel):
        return cls('JOIN', arguments=[channel])

    @classmethod
    def part(cls, channel):
        return cls('PART', arguments=[channel])

    @classmethod
    def nick(cls, new_nick):
        return cls('NICK', arguments=[new_nick])

    @classmethod
    def user(cls, user_name, real_name):
        return cls('USER', arguments=[user_name, '0', '*', real_name])

    @classmethod
    def pong(cls, *args):
        return cls('PONG', arguments=args)

