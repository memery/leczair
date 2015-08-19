import re

from logging import getLogger

from classes import Message
from behaviour import framework


log = getLogger(__name__)


@framework.passive
def run(message, state):
    last_message = state.last_message.get(message.origin)
    log.debug('Last message from %s: %s', message.origin, last_message)
    if last_message:
        subst_re = re.compile(r'^s/(.+)/(.+)/(\w)?$')

        match = subst_re.match(message.text)
        if match:
            del state['last_message'][message.origin]

            corrected = re.sub(match.group(1), match.group(2), last_message)
            log.debug('Corrected message: %s', corrected)

            yield Message.privmsg(
                message.recipient,
                'Corrected message: <{}> {}'.format(message.origin,
                                                    corrected)
            )
    else:
        log.debug('New last message for %s: %s', message.origin, message.text)
        state.last_message[message.origin] = message.text

