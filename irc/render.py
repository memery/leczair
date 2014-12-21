def to_raw(message):
    return '{} {} :{}'.format(message.command,
                              ' '.join(message.arguments[:-1]),
                              message.arguments[-1])
