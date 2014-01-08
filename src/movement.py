from collections import defaultdict

import common
from system import System
from events import *


class MovementComponent(object):
    def __init__(self, entity_id, body, velocity=None, pulse_velocity=None,
                 parent=None):
        self.entity_id = entity_id
        self.body = body 
        self.velocity = velocity
        self.pulse_velocity = pulse_velocity
        self.parent = parent
        self.active = False


class VaryingMovementComponent(object):
    def __init__(self, entity_id, body, velocity_func, pulse_velocity=None,
                 parent=None):
        self.entity_id = entity_id
        self.body = body
        self.velocity_func = velocity_func
        self.pulse_velocity = pulse_velocity
        self.parent = parent
        self.active = False

    @property
    def velocity(self):
        return self.velocity_func()


class MovementSystem(System):
    def __init__(self, factory, components=None):
        super(MovementSystem, self).__init__()
        self.factory = factory
        self.components = defaultdict(list) if components is None else components

    def _add(self, component):
        comp = component
        self.components[comp.parent].append(component)

    def _remove(self, component):
        comp = component
        try:
            self.components[comp.parent].remove(component)
        except ValueError as e:
            print "Not able to remove component from MovementSystem: %s" % e.strerror

    def _activate(self, component):
        comp = component
        # if this component was not already active, apply
        # pulse velocity
        if not comp.active and comp.pulse_velocity:
            comp.body[0] += comp.pulse_velocity[0]
            comp.body[1] += comp.pulse_velocity[1]
        comp.active = True

    def _deactivate(self, component):
        component.active = False

    def _apply_incidental(self, component):
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
        elif event.type == APPLYINCIDENTALMOVEMENTCOMPONENT:
            self._apply_incidental(event.component)

    def update(self, time):
        self.delta = time
        for parent, children in self.components.iteritems():
            for child in [x for x in children if x.active]:
                child.body[0] += child.velocity[0]
                child.body[1] += child.velocity[1]
            if parent is not None:                
                parent.body[0] += parent.velocity[0]
                parent.body[1] += parent.velocity[1]
