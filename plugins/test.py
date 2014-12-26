from irc import Message


def run(message, state):
    if message.text == '.test':
        if state.called:
            return Message(command='PRIVMSG',
                           arguments=[message.recipient,
                                      'You have already tested'])
        else:
            state.called = True
            return Message(command='PRIVMSG',
                           arguments=[message.recipient,
                                      'Testing first time!'])