from collections import defaultdict
from copy import copy


class Event(object):
    def __init__(self, event_type, **kwargs):
        self.event_type = event_type
        for key, value in kwargs.iteritems():
            setattr(self, key, value)


class EventMapping(object):
    def __init__(self):
        self.mapping = defaultdict(list)

    def register_handler(self, event_type, handler):
        self.mapping[event_type].append(handler)

    def remove_handler(self, event_type, handler):
        self.mapping[event_type].remove(handler)

    def __getitem__(self, key):
        return self.mapping[key]


class EventQueue(object):
    def __init__(self):
        self.events = list()

    def push_event(self, event):
        self.events.append(event)

    def get_events(self, event_type=None):
        ret_events = None
        if event_type is None:
            ret_events = copy(self.events)
            self.events = list()
        else:
            ret_events = [x for x in self.events if x.event_type == event_type]
            self.events = list()
        return ret_events

    def peek(self):
        return len(self.events) > 0


class EventManager(object):
    def __init__(self, queue, mapping):
        self.queue = queue
        self.mapping = mapping

    def fire_event(self, event):
        for handler in self.mapping[event.event_type]:
            handler(event)


EVENT_QUEUE = EventQueue()
EVENT_MAPPING = EventMapping()
EVENT_MANAGER = EventManager(EVENT_QUEUE, EVENT_MAPPING)
