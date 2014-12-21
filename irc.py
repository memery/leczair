

def init(sock):
    # send USER, NICK and such
    pass

def manage(raw_msg):
    # if raw_message ~= PING
    #     return PONG
    # if not in channel
    #     return JOIN channel
    # if kicked
    #     remove channel from settings
    pass

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

