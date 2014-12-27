import irc


def run(message, state):
    if message.text == '.test':
        if 'called' in state:
            return privmsg(message.recipient, 'You have already tested')
        else:
            state.called = True
            return privmsg(message.recipient, 'Testing first time!')
