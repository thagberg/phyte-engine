import copy
from events import *
from pygame import event

class BindingComponent(object):
	def __init__(self, entity_id, key):
		self.key = key
		self.hold_time = hold_time


class InputComponent(object):
	def __init__(self, entity_id, bindings):
		self.entity_id = entity_id
		self.bindings = bindings
		self.state = dict.fromkeys(bindings.keys(), False)
		self.last_state = None


class InputSystem(object):
	def __init__(self, components=None):
		self.components = components

	def update(self, time, events=None):
		for comp in self.components:
			comp.last_state = copy.deepcopy(comp.state)

		# process events
		for event in events:
			target = self.components[event.entity_id]

			# keyboard events
			if event.type == event.KEYDOWN:
				name = _lookup_binding(event.key, target.bindings)
				if name is not None:
					target.state[name] = True
			elif event.type == event.KEYUP:
				name = _lookup_binding(event.key, target.bindings)
				if name is not None:
					target.state[name] = False

			# joystick/gamepad events
			elif event.type == event.JOYBUTTONDOWN:
				name = _lookup_binding(event.button, target.bindings)
				if name is not None:
					target.state[name] = True
			elif event.type == event.JOYBUTTONUP:
				name = _lookup_binding(event.button, target.bindings)
				if name is not None:
					target.state[name] = False

			# mouse events
			elif event.type == event.MOUSEBUTTONDOWN:
				name = _lookup_binding(event.button, target.bindings)
				if name is not None:
					target.state[name] = True
			elif event.type == event.MOUSEBUTTONUP:
				name = _lookup_binding(event.button, target.bindings)
				if name is not None:
					target.state[name] = False

			# system events
			elif event.type == ADDINPUTENTITY:
				pass
			elif event.type == REMOVEINPUTENTITY:
				pass
			elif event.type == UPDATEBINDINGS:
				pass

	def _lookup_binding(self, input, bindings):
		for name, binding in bindings.items():
			if input == binding:
				return name
		return None


