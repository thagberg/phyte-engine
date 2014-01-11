from events import *
from system import System
from pygame import event
from collections import defaultdict


class MoveComponent(object):
    def __init__(self, entity_id, name, animation=None, inputs=None,
                 rules=None):
        self.entity_id = entity_id
        self.name = name
        self.animation = animation
        self.inputs = inputs
        self.active = False
        self.rules = list() if rules is None else rules


class MoveSystem(System):
    def __init__(self, factory, components=None):
        self.factory = factory
        self.components = list() if components is None else components
        self.entity_mapping = defaultdict(list)

    def _add(self, component):
        self.components.append(component)
        self.entity_mapping[component.entity_id].append(component)

    def _remove(self, component):
        # clear animation
        if component.animation:
            ra_event = GameEvent(ANIMATIONDEACTIVATE,
                                 component=component.animation)
            self.delegate(ra_event)
        try:
            self.components.remove(component)
            self.entity_mapping[component.entity_id].remove(component)
        except ValueError as e:
            print "Not able to remove component from MoveSystem: %s" % e.strerror

    def _activate(self, component):
        component.active = True
        # an entity may only be engaging in 1 move at a time
        for comp in self.entity_mapping[component.entity_id]:
            if comp != component:
                dm_event = GameEvent(MOVEDEACTIVATE, component=comp)
                self.delegate(dm_event)
        # if a move is activated, its animation must be active as well
        aa_event = GameEvent(ANIMATIONACTIVATE,
                             component=component.animation)
        self.delegate(aa_event)

    def _deactivate(self, component):
        component.active = False
        # if a move is deactivated, its animation must be inactive as well
        da_event = GameEvent(ANIMATIONDEACTIVATE,
                             component=component.animation)
        self.delegate(da_event)

    def handle_event(self, event):
        if event.type == ADDMOVECOMPONENT:
            self._add(event.component)
            print "Added new MoveComponent: %s" % event.component
        elif event.type == REMOVEMOVECOMPONENT:
            self._remove(event.component)
            print "Removed MoveComponent: %s" % event.component
        elif event.type == MOVEACTIVATE:
            self._activate(event.component)
        elif event.type == MOVEDEACTIVATE:
            self._deactivate(event.component)

    def update(self, time):
        self.delta = time
        # iterate over active move components
        for comp in [x for x in self.components if x.active]:
            pass
