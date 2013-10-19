from system import System
from events import *

class PlayerComponent(object):
    def __init__(self, entity_id, location, moves=None, inputs=None, 
                 graphic=None, input_device=-1):
        self.entity_id = entity_id
        self.location = location
        self.moves = list() if moves is None else moves
        self.inputs = inputs
        self.graphic = graphic
        self.input_device = input_device


class PlayerSystem(System):
    def __init__(self, factory, components=None):
        self.factory = factory
        self.components = list() if components is None else components

    def _add(self, component):
        self.components.append(component)

    def _remove(self, component):
        c = component
        # clear player moves
        for move in c.moves:
            rm_event = GameEvent(MOVEDEACTIVATE, component=move)
            self.delegate(rm_event)
        # clear graphic
        if self.graphic:
            rg_event = GameEvent(REMOVEGRAPHICSCOMPONENT,
                                 component=self.graphic)
            self.delegate(rg_event)
        # clear inputs
        if self.inputs:
            ri_event = GameEvent(REMOVEINPUTCOMPONENT,
                                 device=self.input_device, 
                                 component=self.inputs)

    def handle_event(self, event):
        if event.type == ADDPLAYERCOMPONENT:
            self._add(event.component)
        elif event.type == REMOVEPLAYERCOMPONENT:
            self._remove(event.component)

    def update(self, time):
        self.delta = time
        for comp in self.components:
            if comp.inputs.state['left']:
                comp.location.x -= 10
            if comp.inputs.state['right']:
                comp.location.x += 10
