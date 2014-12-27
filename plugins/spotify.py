import re
import xml.etree.ElementTree as ET

from urllib.error import HTTPError, URLError

from classes import Message
from behaviour import framework


def run(message, command_prefix, state):
    spotify_url_re = re.compile(r'spotify(:\S+)+?')

    titles = set(spotify_title(m.group(0))
                 for m in spotify_url_re.finditer(message.text))

    yield from (Message.privmsg(message.recipient, 'Spotify: ' + title)
                for title in titles if title)


def spotify_title(uri):
    spotify_lookup_url = 'http://ws.spotify.com/lookup/1/?uri='

    try:
        xml_str = framework.read_url(spotify_lookup_url + uri,
                                     content_whitelist=['application/xml'])

        root = ET.fromstring(re.sub(' xmlns="[^"]+"', '', xml_str, count=1))
    except (ET.ParseError, HTTPError):
        return None

    if 'album' in uri:
        album_name = root.find('name').text
        artist_name = root.find('artist').find('name').text
        released = root.find('released').text

        return '{}: {} ({})'.format(artist_name, album_name, released)
    elif 'artist' in uri:
        return root.find('name').text
    elif 'track' in uri:
        track_name = root.find('name').text
        artist_name = root.find('artist').find('name').text
        track_time_in_seconds = float(root.find('length').text)
        m, s = divmod(round(track_time_in_seconds), 60)

        return '{} - {} ({}:{})'.format(artist_name, track_name, m, s)
