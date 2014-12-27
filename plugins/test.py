from classes import Message


def run(message, state):
    if message.text == '.test':
        if 'called' in state:
            return Message.privmsg(message.recipient, 'You have already tested')
        else:
            state.called = True
            return Message.privmsg(message.recipient, 'Testing first time!')
