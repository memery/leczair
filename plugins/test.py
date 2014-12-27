from irc import Message
from behaviour import framework


@framework.command('test')
def run(message, arguments, state):
    if 'called' in state:
        yield Message(command='PRIVMSG',
                       arguments=[message.recipient,
                                  'You have already tested'])
    else:
        state.called = True
        yield Message(command='PRIVMSG',
                      arguments=[message.recipient,
                                 'Testing first time!'])
