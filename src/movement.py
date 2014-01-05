import common
from system import System
from events import *


class MovementComponent(object):
    def __init__(self, entity_id, body, velocity=None):
        self.entity_id = entity_id
        self.body = body 
        self.velocity = velocity
        self.active = False


class VaryingMovementComponent(object):
    def __init__(self, entity_id, body, velocity_func):
        self.entity_id = entity_id
        self.body = body
        self.velocity_func = velocity_func
        self.active = False

    @property
    def velocity(self):
        return self.velocity_func()


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
        comp = component
        comp.active = True

    def _deactivate(self, component):
        component.active = False

    def _add_incidental(self, component):
        component.body[0] += component.velocity[0]
        component.body[1] += component.velocity[1]

    def handle_event(self, event):
        if event.type == ADDMOVEMENTCOMPONENT:
            self._add(event.component)
        elif event.type == REMOVEMOVEMENTCOMPONENT:
            self._remove(event.component)
        elif event.type == ACTIVATEMOVEMENTCOMPONENT:
            self._activate(event.component)
        elif event.type == DEACTIVATEMOVEMENTCOMPONENT:
            self._deactivate(event.component)
        elif event.type == ADDINCIDENTALMOVEMENTCOMPONENT:
            self._add_incidental(event.component)

    def update(self, time):
        self.delta = time
        for comp in [x for x in self.components if x.active]:
            comp.body[0] += comp.velocity[0]
            comp.body[1] += comp.velocity[1]
