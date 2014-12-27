from classes import Message
from behaviour import framework

@framework.command('test')
def run(message, arguments, state):
    if 'called' in state:
        yield Message.privmsg(message.recipient, 'You have already tested')
    else:
        state.called = True
        yield Message.privmsg(message.recipient, 'Testing first time!')
