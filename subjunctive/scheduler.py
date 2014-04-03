import logging
import re

from sdl2.timer import SDL_GetTicks

class Scheduler:
    def __init__(self):
        self._new_items = []
        self._items = []

    def call(self, function, *, after=None, every=None):
        if after is None and every is None:
            raise TypeError("call() needs at least one keyword argument")
        if after is not None:
            after = ms(after)
        if every is not None:
            every = ms(every)
        self._new_items.append((function, after, every))

    def update(self):
        time = SDL_GetTicks()

        for func, after, every in self._new_items:
            trigger_time = time + after if after else time
            logging.debug("[scheduler] Scheduling {} for {}"
                          "".format(func.__qualname__, trigger_time))
            self._items.append((trigger_time, func, every))
        self._new_items.clear()

        remaining_items = []
        for trigger_time, func, every in self._items:
            if time >= trigger_time:
                logging.debug("[scheduler] Calling {}"
                              "".format(func.__qualname__))
                func()
                if every is not None:
                    new_trigger_time = time + every
                    logging.debug("[scheduler] Scheduling {} for {}"
                                  "".format(func.__qualname__, trigger_time))
                    remaining_items.append((new_trigger_time, func, every))
            else:
                remaining_items.append((trigger_time, func, every))
        self._items = remaining_items

def ms(timespec):
    match = re.match(r'(?P<magnitude>[0-9]+)(?P<unit>ms|s|m)', timespec)
    if not match:
        raise ValueError("Invalid timespec {!r}".format(timespec))
    magnitude, unit = match.group('magnitude', 'unit')
    return int(magnitude) * {'ms': 1, 's': 1000, 'm': 60000}[unit]

_default_scheduler = Scheduler()
call = _default_scheduler.call
update = _default_scheduler.update
