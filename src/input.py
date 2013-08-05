import copy
from collections import defaultdict
from events import *
from pygame import event

#joystick ids start at 0, so using -1 lets us use a universal device id system
KEYB_MOUSE = -1 

class BindingComponent(object):
	def __init__(self, entity_id, key, active=False, hold_time=0):
		self.key = key
		self.active = active
		self.hold_time = hold_time


class Input(object):
	def __init__(self):
		self.name = None
		self.time_since_input = 0	

		
class InputComponent(object):
	def __init__(self, entity_id, bindings):
		self.entity_id = entity_id
		self.bindings = bindings
		self.state = dict.fromkeys(bindings.keys(), False)
		self.last_state = None


class InputSystem(object):
	"""InputSystem manages the state of InputComponents which hold the
		bindings of keys/buttons to game actions"""

	def __init__(self, components=None):
		# a map of lists, map keys are input devices, list items are
		#   components mapped to that device
		self.components = defaultdict(list) if components is None else components

	def update(self, time, events=None):
		for device, components in self.components.items():
			for comp in components:
				comp.last_state = copy.deepcopy(comp.state)

		for event in events:
			target = self.components[event.entity_id]

			# system events
			if event.type == ADDINPUTCOMPONENT:
				self.components[event.device].append(event.component)
			elif event.type == REMOVEINPUTCOMPONENT:
				self.components[event.device].remove(event.component)
			elif event.type == UPDATEBINDINGS:
				pass

			# keyboard events
			elif event.type == event.KEYDOWN:
				self._apply_key_down(KEYB_MOUSE, event.key)
			elif event.type == event.KEYUP:
				self._apply_key_up(KEYB_MOUSE, event.key)

			# joystick/gamepad events
			elif event.type == event.JOYBUTTONDOWN:
				self._apply_key_down(event.joy, event.button)
			elif event.type == event.JOYBUTTONUP:
				self._apply_key_up(event.joy, event.button)

			# mouse events
			elif event.type == event.MOUSEBUTTONDOWN:
				self._apply_key_down(KEYB_MOUSE, event.button)
			elif event.type == event.MOUSEBUTTONUP:
				self._apply_key_up(KEYB_MOUSE, event.button)


	def _apply_key_down(self, device, key):
		components = self.components[device]
		for component in components:
			binding = component.bindings
			bind = self._lookup_binding(key, binding)	
			if bind is None:
				continue
			component.state[bind] = True

	def _apply_key_up(self, device, key):	
		components = self.components[device]
		for component in components:
			binding = component.bindings
			bind = self._lookup_binding(key, binding)
			if bind is None:
				continue
			component.state[bind] = False

	def _lookup_binding(self, input, bindings):
		for name, binding in bindings.items():
			if input == binding:
				return name
		return None


class InputBufferComponent(object):
	def __init__(self, entity_id, expire_time):
		self.entity_id = entity_id
		self.buffer = list()
		self.expire_time = expire_time	


class InputBufferSystem(object):
	"""InputBufferSystem manages InputBufferComponents which hold the buffered
	   inputs from a player, and allow for time-based expiration of inputs from buffer"""

	def __init__(self, components=None):
		self.components = list() if components is None else components

	def update(self, time, events=None):
		for event in events:
			if event.type == ADDINPUTBUFFERCOMPONENT:
				self.components.add(event.buffer)
			elif event.type == REMOVEINPUTBUFFERCOMPONENT:
				self.components.remove(event.buffer)
			elif event.type == BUFFERINPUT:
				if not self.components[event.entity_id] is None:
					self.components[event.entity_id].buffer.append(event.input)

		for component in self.components:

	def _expire_inputs(self, time_delta, buffered_inputs, expire_time):
		for bi in buffered_inputs:
			if not bi.active:


