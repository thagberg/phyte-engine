from system import System
from events import *
from collections import defaultdict


NORMAL_INPUT_MAPPING = {
    'forward': 'right',
    'backward': 'left'
}
MIRROR_INPUT_MAPPING = {
    'forward': 'left',
    'backward': 'right'
}

class ExecutionComponent(object):
    def __init__(self, entity_id, executables, inputs, 
                 mirror=False, active=False):
        self.entity_id = entity_id
        # NOTE: executables should be ordered based on priority
        self.executables = list() if executables is None else executables
        self.inputs = inputs
        self.mirror = mirror
        self.active = active


class ExecutionSystem(System):
    def __init__(self, factory, components=None):
        super(ExecutionSystem, self).__init__()
        self.factory = factory
        self.components = list() if components is None else components
        self.entity_mapping = defaultdict(list)

    def _add(self, component):
        self.components.append(component)
        self.entity_mapping[component.entity_id].append(component) 

    def _remove(self, component):
        try:
            self.components.remove(component)
            self.entity_mapping[component.entity_id].remove(component)
        except ValueError as e:
            print "Not able to remove component from ExecutionSystem: %s" % e.strerror

    def _build_entity_mapping(self):
        self.entity_mapping = defaultdict(list)
        em = self.entity_mapping
        for comp in self.components:
            em[comp.entity_id].append(comp)

    def _activate(self, component):
        component.active = True

    def _deactivate(self, component):
        component.active = False

    def _activate_by_entity(self, entity_id):
        comps = self.entity_mapping[entity_id]
        for comp in comps:
            comp.active = True

    def _deactivate_by_entity(self, entity_id):
        comps = self.entity_mapping[entity_id]
        for comp in comps:
            comp.active = False

    def _clean_input(self, dirty_input, mirror):
        clean_input = dirty_input
        return clean_input
        #TODO maybe get rid of this stuff; I'm thinking that
        # this should be handled within the input system
        if mirror:
            if clean_input in MIRROR_INPUT_MAPPING:
                clean_input = MIRROR_INPUT_MAPPING[clean_input]
        else:
            if clean_input in NORMAL_INPUT_MAPPING:
                clean_input = NORMAL_INPUT_MAPPING[clean_input]
        return clean_input 

    def _check_for_move(self, executables, inputs):
        '''
            Given a list of moves (executables), and the current input state
            (including an input buffer) try to find a move which has been
            executed.  Moves should be listed by priority, decreasing
        '''
        inp_buffer = inputs.inp_buffer
        for ex in executables:
            # loop over the executable's inputs and verify that the
            # current input state covers each of them
            match = True
            # if length of inputs is greater than 1, this is a buffered move
            if len(ex.inputs) > 1:
                match_index = 0
                required_inp = ex.inputs[match_index]
                # loop over each input in the existing buffer
                for buffered_inp in inp_buffer:
                    # if the current required input finds a match in the buffer,
                    # increase the match index
                    if buffered_inp == inp:
                        match_index += 1
                    # if the match index exceeds the length of the inputs
                    # we are looking for, then each input has been satisfied
                    # and this move has been executed
                    if match_index >= len(ex.inputs):
                        return ex
                    # otherwise, check for the next required input
                    else: 
                        required_inp = ex.inputs[match_index]
            else:
                for frame_inputs in ex.inputs:
                    for inp in frame_inputs:
                        if not inputs.state[inp]:
                            match = False
                            break
                if match:
                    return ex
        # no match found, no move executed
        return None 

    def _change_mirror(entity_id, mirror):
        '''
            DEPRECATED
        '''
        comps = [x for x in self.components if x.entity_id == entity_id]
        for c in comps:
            c.mirror = mirror

    def handle_event(self, event):
        if event.type == ADDEXECUTIONCOMPONENT:
            self._add(event.component)
            print "Added new ExecutionComponent: %s" % event.component
        elif event.type == REMOVEEXECUTIONCOMPONENT:
            self._remove(event.component)
            print "Removed ExecutionComponent: %s" % event.component
        elif event.type == ACTIVATEEXECUTIONCOMPONENT:
            self._activate(event.component)
        elif event.type == DEACTIVATEEXECUTIONCOMPONENT:
            self._deactivate(event.component)
        elif event.type == FACINGCHANGE:
            self._change_mirror(event.entity_id, event.mirror)

    def update(self, time):
        self.delta = time
        # iterate only over the active components
        for comp in [x for x in self.components if x.active]:
            execute = self._check_for_move(comp.executables, comp.inputs)
            if execute and not execute.active:
                ma_event = GameEvent(MOVEACTIVATE, component=execute)
                self.delegate(ma_event)
                break


class BufferedExecutionSystem(ExecutionSystem):
    '''
        DEPRECATED
    '''
    def __init__(self, factory, components=None):
        super(BufferedExecutionSystem, self).__init__(factory, components) 

    def _check_for_move(self, executables, input_buffer, mirror):
        buf = input_buffer
        for ex in executables:
            input_index = 0
            # if input is forward/backward, translate it to proper 
            # directional input
            clean = self._clean_input(ex.inputs[input_index], mirror)
            for inp in buf: 
                # check if this buffered input matches the next
                # input value for this executable
                if inp == clean:
                    input_index += 1
                if input_index >= len(ex.inputs):
                    return ex
                else:
                    clean = this.clean_input(ex.inputs[input_index], mirror)
        # no executable matched to input buffer
        return None

    def handle_event(self, event):
        if event.type == ADDBUFFEREDEXECUTIONCOMPONENT:
            self._add(event.component)
        elif event.type == REMOVEBUFFEREDEXECUTIONCOMPONENT:
            self._remove(event.component)
        elif event.type == ACTIVATEBUFFEREDEXECUTIONCOMPONENT:
            self._activate(event.component)
        elif event.type == DEACTIVATEBUFFEREDEXECUTIONCOMPONENT:
            self._deactivate(event.component)
        elif event.type == FACINGCHANGE:
            self._change_mirror(event.entity_id, event.mirror)

    def update(self, time):
        self.delta = time
        # iterate only over the active components
        for comp in [x for x in self.components if x.active]:
            execute = self._check_for_move(comp.executables,
                                           comp.inputs.input_buffer, comp.mirror)
            if execute:
                ma_event = GameEvent(MOVEACTIVATE, component=execute)
                self.delegate(ma_event)
                break


