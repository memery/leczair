

def init(sock, state):
    irc_settings = state.settings.irc
    sock.write('NICK {}'.format(irc_settings.nick))
    sock.write('USER {0} 0 * :IRC bot {0}'.format(irc_settings.nick))
    state.irc.joined = False


def manage(raw_msg, state):
    if message.command == 'PING':
        # return PONG message
        pass
    elif message.command == '403':
        # Channel doesn't exist, stop trying to join
        state.settings.irc.channel = None


def get_message(sock):
    # raw_message = sock.get()
    # if response = manage(raw_message)
    #     send_message(response)
    #     return None
    # else:
    #     return to_internal_message(raw_message)
    pass


def send_message(sock, msg):
    # socket.send(to_raw_message(internal_message))
    pass

