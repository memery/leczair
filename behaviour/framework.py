from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


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
