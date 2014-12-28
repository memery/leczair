import re
import heapq
import logging

from datetime import datetime, timedelta

from classes import Message
from behaviour import framework


logger = logging.getLogger(__name__)


class Heap:
    _heap = []

    def push(self, value):
        heapq.heappush(self._heap, value)

    def pop(self):
        return heapq.heappop(self._heap)


@framework.command('remind', split_arguments=False)
def _command(message, arguments, state):

    match = re.fullmatch(
        r'^(.+) (in|on|at) (.+) with "(.+)"',
        arguments
    )

    if match:
        if not state.subscriptions:
            state.subscriptions = Heap()

        who = match.group(1)
        if who == 'me':
            who = message.origin

        preposition = match.group(2)
        when = match.group(3)
        try:
            if preposition == 'in':
                when = when.split(':')
                when = datetime.now() + timedelta(hours=int(when[0]),
                                                  minutes=int(when[1]))
            elif preposition == 'on':
                when = datetime.strptime('%Y-%m-%d', when)
            elif preposition == 'at':
                now = datetime.now()
                when = when.split(':')

                now.hour = int(when[0])
                now.minute = int(when[0])

                when = now
        except Exception as e:
            logger.exception(e)
            yield Message.privmsg(message.recipient, message.origin
                                  + ': Come again?')
            return

        what = match.group(4)

        state.subscriptions.push((when, who, preposition, what))

        yield Message.privmsg(message.recipient, message.origin
                              + ': You betcha')

        
@framework.passive_with_command(_command)
def run(message, state):
    if state.subscriptions:
        try:
            when, who, preposition, what = state.subscriptions.pop()
        except IndexError:
            logger.debug("Didn't remind anybody")
            return
        else:
            if when >= datetime.now():
                yield Message.privmsg(message.recipient,
                                      '{}: Reminder: {}'.format(who, what))
            else:
                state.subscriptions.push((when, who, preposition, what))
    else:
        logger.debug("Didn't remind anybody")
