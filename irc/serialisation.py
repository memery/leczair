
import re
from message import Message


user_pattern = re.compile(r':([^ ]+) ')
command_pattern = re.compile(r'([^ ]+)')
argument_pattern = re.compile(r' ([^:][^ ]*)')
last_arg_pattern = re.compile(r' :(.*)')
nick_pattern = re.compile(r'~?([^!]+)!')


def from_raw(raw_message):

    """
    Deserialises an inbound message, returning a Message object.

    """

    user, command, args, last_arg = basic_parse(raw_message)
    if last_arg:
        args.append(last_arg)
    message = Message(command, arguments=args)
    message.user = user
    return message


def to_raw(message):

    """
    Serialises an outbound message to a string the server would like to have.
    
    """

    *args, last_arg = message.arguments
    return '{} {} :{}'.format(message.command, ' '.join(args), last_arg)


def basic_parse(raw_message):

    """
    A generator that yields components from a raw IRC network message.

    """

    parser_chain = [parse_one(user_pattern),
                    parse_one(command_pattern),
                    parse_many(argument_pattern),
                    parse_one(last_arg_pattern)]
    
    rest = raw_message
    for parser in parser_chain:
        parse, rest = parser(rest)
        yield parse


def parse_one(pattern):
    
    """
    Given a pattern and some text to parse, parse_one will
    do one of two things:
        1. If there is no match at the start of text for pattern,
           return the tuple of None and the original text
        2. If there is a match, return the match and the rest
           of the text without the match in it.

    Curried because it makes the code using it nicer.

    """

    def run_parser(text):
        m = pattern.match(text)
        if m:
            return m.group(1), text[m.end(0):]
        else:
            return None, text

    return run_parser


def parse_many(pattern):
    
    """
    parse_many works like parse_one except it will consume
    as many matches as it can before returning a list of
    them all.

    """

    def run_parser(text):
        parsed = []
        m = pattern.match(text)
        rest = text
        while m and rest:
            current, rest = parse_one(pattern)(rest)
            if current:
                parsed.append(current)
            else:
                break

        return parsed, rest

    return run_parser

