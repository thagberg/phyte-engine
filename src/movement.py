import common
from system import System
from events import *


class MovementComponent(object):
    def __init__(self, entity_id, body, velocity, inc_velocity):
        self.entity_id = entity_id
        self.body = body 
        self.velocity = velocity
        # incidental velocity (happens when component is first activated)
        #   not applied on each update
        self.inc_velocity = inc_velocity
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
        comp = component
        # if this component was not already active, apply
        # incidental velocity
        if not comp.active and comp.inc_velocity:
            comp.body[0] += comp.inc_velocity[0]
            comp.body[1] += comp.inc_velocity[1]
        comp.active = True

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
            comp.body[0] += comp.velocity[0]
            comp.body[1] += comp.velocity[1]
