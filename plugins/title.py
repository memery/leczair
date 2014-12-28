import re

from html.parser import HTMLParser
from urllib.error import HTTPError, URLError

from irc import Message
from behaviour import framework


@framework.passive
def run(message, state):
    url_re = re.compile(r'https?://\S+')

    yield from (Message(command='PRIVMSG',
                        arguments=[message.recipient, title])
                for title in set(html_title(url)
                                 for url in url_re.findall(message.text)))


def html_title(url):
    unescape_html = HTMLParser().unescape

    title_re = re.compile(r'<title.*?>(.+?)</title>')

    content = framework.read_url(url, content_whitelist=['text/html'])
    if content:
        title = title_re.search(content, re.IGNORECASE | re.DOTALL)
        if title:
            return unescape_html(title.group(1).strip())
