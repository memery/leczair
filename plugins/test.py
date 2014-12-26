from irc import Message


def run(message):
    return Message(command='PRIVMSG', arguments=['#leczair', 'Testar!'])
