import common
from system import System
from events import *


class ForceComponent(object):
    def __init__(self, entity_id, body, force):
        self.entity_id = entity_id
        self.body = body
        self.force = force


class ForceSystem(System):
    def __init__(self, factory, components=None):
        super(ForceSystem, self).__init__()
        self.factory = factory
        self.components = list() if components is None else components

    def _add(self, component):
        self.components.append(component)

    def _remove(self, component):
        try:
            self.components.remove(component)
        except ValueError as e:
            print "Not able to remove component from ForceSystem: %s" % e

    def handle_event(self, event):
        if event.type == ADDFORCECOMPONENT:
            self._add(event.component)
        elif event.type == REMOVEFORCECOMPONENT:
            self._remove(event.component)

    def update(self, time):
        self.delta = time
        for comp in self.components:
            comp.body[0] += comp.force[0]
            comp.body[1] += comp.force[1]