from system import System
from events import *
from collections import defaultdict
from copy import deepcopy

class PlayerComponent(object):
    def __init__(self, entity_id, location, opponent=None, buffered_moves=None, 
                 immediate_moves=None, inputs=None, graphic=None, 
                 input_device=-1):
        self.entity_id = entity_id
        self.opponent = opponent
        self.location = location
        if buffered_moves:
            self.buffered_moves = buffered_moves
        else:
            self.buffered_moves = list()
        if immediate_moves:
            self.immediate_moves = immediate_moves
        else:
            self.immediate_moves = defaultdict(list)
        self.inputs = inputs
        self.graphic = graphic
        self.input_device = input_device
        self.states = list()
        self.on_ground = False
        self.attacking = False
        self.under_attack = False
        self.facing_left = False
        self.hitstun = 0


class PlayerStates(object):
    STANDING = 0
    WALKING = 1
    CROUCHING = 2
    JUMPING = 3
    FALLING = 4
    BACKING = 5
    HITSTUN = 6


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
        if c.graphic:
            rg_event = GameEvent(REMOVEGRAPHICSCOMPONENT,
                                 component=c.graphic)
            self.delegate(rg_event)
        # clear inputs
        if c.inputs:
            ri_event = GameEvent(REMOVEINPUTCOMPONENT,
                                 device=c.input_device, 
                                 component=c.inputs)
            self.delegate(ri_event)
        # remove player
        try:
            self.components.remove(c)
        except ValueError as e:
            print "Not able to remove component from PlayerSystem: %s" % e.strerror

    def _find_player_state(self, component):
        c = component
        fl = c.facing_left

    def _find_player_state_OLD(self, component):
        c = component
        fl = c.facing_left
        # get a copy of previous frame states and then start fresh
        old_state = deepcopy(c.states)
        c.states = list()
        # is player on the ground
        if c.on_ground:
            # is player attacking
            if not(c.attacking):
                # is player currently in hit stun
                if c.hitstun > 0:
                    c.states.append(PlayerStates.HITSTUN)
                    if PlayerStates.CROUCHING in old_state:
                        c.states.append(PlayerStates.CROUCHING) 
                    else:
                        c.states.append(PlayerStates.STANDING)                        
                else:
                    # on ground, not attacking, not in hit stun
                    # first let's see if we're moving
                    if c.inputs.state['down']:
                        c.states.append(PlayerStates.CROUCHING)
                        if c.inputs.state['left']:
                            if not fl:
                                c.states.append(PlayerStates.BLOCKING)
                        if c.inputs.state['right']:
                            if fl:
                                c.states.append(PlayerStates.BLOCKING)
                    else:
                        c.states.append(PlayerStates.STANDING)
                        if c.inputs.state['left']:
                            if fl:
                                c.states.append(PlayerState.WALKING)
                            else:
                                if c.opponent and c.opponent.attacking:
                                    c.states.append(PlayerStates.BLOCKING)
                                else:
                                    c.states.append(PlayerStates.BACKING)
                        elif c.inputs.state['right']:
                            if fl:
                                if c.opponent and c.opponent.attacking:
                                    c.states.append(PlayerStates.BLOCKING)
                                else:
                                    c.states.append(PlayerStates.BACKING)
                            else:
                                c.states.append(PlayerStates.WALKING)
                    # as long as the player's not attacking or being attacked,
                    # it can start a jump
                    if c.inputs.state['up']:
                        c.states.append(PlayerStates.JUMPING)
        else:
            pass

    def handle_event(self, event):
        if event.type == ADDPLAYERCOMPONENT:
            self._add(event.component)
        elif event.type == REMOVEPLAYERCOMPONENT:
            self._remove(event.component)
        elif event.type == MOVEDEACTIVATE:
            pass

    def update(self, time):
        self.delta = time
        for comp in self.components:
            if comp.inputs.state['left']:
                comp.location.x -= 10
            if comp.inputs.state['right']:
                comp.location.x += 10
