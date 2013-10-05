from collections import defaultdict
from events import *
import pygame

class SystemEntity(object):
    def __init__(self, system, event_types=None):
        self.system = system
        self.event_types = list() if event_types is None else event_types

class PygameEngine(object):
    def __init__(self, systems=None):
        self.systems = list() if systems is None else systems
        self.system_event_map = defaultdict(list)

    def install_system(self, system, event_types=None):
        system.attach_delegate(self.process_event)
        new_system = SystemEntity(system, event_types)
        self.systems.append(new_system)
        for e_type in event_types:
            self.system_event_map[e_type].append(system)

    def process_event(self, event):
        handlers = self.system_event_map[event.type]
        for handler in handlers:
            handler.handle_event(event)

    def update(self, time, events):
        for event in events:
            parsed_event = None
            if event.type == pygame.KEYDOWN:
                parsed_event = GameEvent(KEYDOWN, key=event.key)
            elif event.type == pygame.KEYUP:
                parsed_event = GameEvent(KEYUP, key=event.key)
            elif event.type == pygame.JOYBUTTONDOWN:
                parsed_event = GameEvent(JOYBUTTONDOWN, joy=event.joy,
                                         button=event.button)   
            elif event.type == pygame.JOYBUTTONUP:
                parsed_event = GameEvent(JOYBUTTONUP, joy=event.joy,
                                         button=event.button)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                parsed_event = GameEvent(MOUSEBUTTONDOWN, pos=event.pos,
                                         button=event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                parsed_event = GameEvent(MOUSEBUTTONUP, pos=event.pos,
                                         button=event.button)
            elif event.type == pygame.JOYAXISMOTION:
                parsed_event = GameEvent(JOYAXISMOTION, joy=event.joy, 
                                         axis=event.axis, value=event.value)

            if parsed_event:
                self.process_event(parsed_event)
        for sys in self.systems:
            sys.system.update(time)
            # TODO: investigate more efficient ways of filtering
            #   the events list; possibly list comprehensions
            #sys.system.update(time, filter(lambda x: x.type in sys.event_types or (hasattr(x, 'u_type') and x.u_type in sys.event_types), events))
