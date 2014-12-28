from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from functools import wraps


def passive(run):

    """
    Makes the entry-point in a plugin passive. Basically it only gets rid
    of the command_prefix-argument.

    Usage:
      @framework.passive
      def run(message, state):
          # stuff

    """

    @wraps(run)
    def wrapper(message, command_prefix, state):
        return run(message, state)

    return wrapper


def passive_with_command(command_fn):

    """
    Makes the entry point in a plugin passive, but yields specified
    command function first.

    Note that the command function should be defined just like any command.

    Usage:
      @framework.passive_with_command(mycommand)
      def run(message, state):
          # stuff

    """

    def decorator(run):
        @wraps(run)
        def wrapper(message, command_prefix, state):
            yield from command_fn(message, command_prefix, state)
            yield from run(message, state)

        return wrapper

    return decorator


def command(name, split_arguments=True):

    """
    Makes a function into a command that can be used in a plugin. For
    example the entry-point.

    `split_arguments` specifies whether arguments should be represented
    like a string or splitted into a list.

    Usage:
      @framework.command('mycommand')
      def run(message, arguments, state):
          # stuff

    """

    def decorator(run):
        @wraps(run)
        def wrapper(message, command_prefix, state):
            try:
                command, arguments = message.text.split(maxsplit=1)
            except ValueError:
                command = message.text
                arguments = ''

            if split_arguments:
                arguments = arguments.split()

            if command == command_prefix + name:
                return run(message, arguments, state)
            else:
                return () # default to empty iterable

        return wrapper

    return decorator


# TODO: This is straight from memery-legacy. It should be overlooked.

def url_request(url):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 memery')
    return req


def read_url(url, args='', quote_=True, content_whitelist=[]):

    """
    Return the data (presumably text) from a url and decode it to utf-8 using
    the page's preferred encoding (if found).

    args -- a suffix argument that will be appended to the url
    quote_ -- if True, will mean that args will be appended as quote(args)
    content_whitelist -- a list of MIME types which the page's type has to be
                         one of (empty list means no restriction)

    """

    # Convert non-ascii chars to %xx-format
    safe = '/:;.,?+-=@#&' # These will not be converted
    url = quote(url, safe)

    # Handy thing to append stuff to the url with a valid format
    if args:
        if quote_:
            args = quote(args)
        url += str(args)

    # Read the page and try to find the encoding in the headers
    encoding = None
    with urlopen(url_request(url)) as s:
        if content_whitelist and s.info().get_content_type() \
           not in content_whitelist:
            return None
        # This may return None
        encoding = s.info().get_content_charset()
        page = s.read()

    # Get the encoding of the page manually if there's no header
    if not encoding:
        metatag_encoding = re.search(b'<meta.+?charset="?(.+?)["; ].*?>', page)
        if metatag_encoding:
            encoding = metatag_encoding.group(1).decode()

    if encoding:
        content = page.decode(encoding, 'replace')
    # Fallback, in case there is no known encoding
    else:
        try:
            content = page.decode('utf-8')
        except:
            content = page.decode('latin-1', 'replace')

    return content
