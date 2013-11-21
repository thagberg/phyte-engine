import common
from system import System
from events import *


class MovementComponent(object):
    def __init__(self, entity_id, location, velocity):
        self.entity_id = entity_id
        self.location = location
        self.velocity = velocity
        self.active = False


class MovementSystem(System):
    def __init__(self, factory, components=None):
        super(MovementSystem, self).__init__()
        self.factory = factory
        self.components = list() if components is None else components

    def _add(self, component):
        self.components.append(component)

    def _remove(self, component):
        try:
            self.components.remove(component)
        except ValueError as e:
            print "Not able to remove component from MovementSystem: %s" % e.strerror

    def _activate(self, component):
        component.active = True

    def _deactivate(self, component):
        component.active = False

    def handle_event(self, event):
        if event.type == ADDMOVEMENTCOMPONENT:
            self._add(event.component)
        elif event.type == REMOVEMOVEMENTCOMPONENT:
            self._remove(event.component)
        elif event.type == ACTIVATEMOVEMENTCOMPONENT:
            self._activate(event.component)
        elif event.type == DEACTIVATEMOVEMENTCOMPONENT:
            self._deactivate(event.component)

    def update(self, time):
        self.delta = time
        for comp in [x for x in self.components if x.active]:
            comp.location[0] += comp.velocity[0]
            comp.location[1] += comp.velocity[1]
