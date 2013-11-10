from system import System
from events import *
from collections import defaultdict


class ExecutionComponent(object):
    def __init__(self, entity_id, executables, inputs, 
                 mirror=False, active=False):
        self.entity_id = entity_id
        # NOTE: executables should be ordered based on priority
        self.executables = list() if executables is None else executables
        self.input = inputs
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
        if mirror:
            if clean_input == 'forward':
                clean_input = 'left'
            elif clean_input == 'backward':
                clean_input = 'right'
        else:
            if clean_input == 'forward':
                clean_input = 'right'
            elif clean_input == 'backward':
                clean_input = 'left'
        return clean_input 

    def _check_for_move(self, executables, input, mirror):
        for ex in executables:
            # loop over the executable's inputs and verify that the
            # current input state covers each of them
            match = True
            for ex_input in ex.inputs:
                clean_input = self._clean_input(ex_input, mirror)
                if not input[clean_input]:
                    match = False
                    break
            if match:
                return ex
        return None 

    def _change_mirror(entity_id, mirror):
        comps = [x for x in self.components if x.entity_id == entity_id]
        for c in comps:
            c.mirror = mirror

    def handle_event(self, event):
        if event.type == ADDEXECUTIONCOMPONENT:
            self._add(event.component)
        elif event.type == REMOVEEXECUTIONCOMPONENT:
            self._remove(event.component)
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
            execute = _check_for_move(comp.executables,
                                      comp.inputs, comp.mirror)
            if execute:
                ma_event = GameEvent(MOVEACTIVATE, component=execute)
                self.delegate(ma_evnet)
                break


class BufferedExecutionSystem(ExecutionSystem):
    def __init__(self, factory, components=None):
        super(BufferedExecutionSystem, self).__init__(factory, components) 

    def _check_for_move(self, executables, input_buffer, mirror):
        buf = input_buffer
        for ex in executables:
            input_index = 0
            # if input is forward/backward, translate it to proper 
            # directional input
            clean = this.clean_input(ex.inputs[input_index], mirror)
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
            execute = _check_for_move(comp.executables,
                                      comp.inputs.input_buffer, comp.mirror)
            if execute:
                ma_event = GameEvent(MOVEACTIVATE, component=execute)
                self.delegate(ma_event)
                break


