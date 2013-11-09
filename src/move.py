from events import *
from pygame import event


class MoveComponent(object):
	def __init__(self, entity_id, name, animation=None, inputs=None,
				 rules=None):
		self.entity_id = entity_id
		self.name = name
		self.animation = animation
		self.inputs = inputs
		self.active = False
		self.rules = list() if rules is None else rules


class MoveSystem(object):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = list() if components is None else components

	def _add(self, component):
		self.components.append(component)

	def _remove(self, component):
		# clear animation
		if component.animation:
			ra_event = GameEvent(ANIMATIONDEACTIVATE,
								 component=component.animation)
			self.delegate(ra_event)
		try:
			self.components.remove(component)
		except ValueError as e:
			print "Not able to remove component from MoveSystem: %s" % e.strerror

	def _activate(self, component):
		component.active = True

	def _deactivate(self, component):
		component.active = False

	def handle_event(self, event):
		if event.type == ADDMOVECOMPONENT:
			self._add(event.component)
		elif event.type == REMOVEMOVECOMPONENT:
			self._remove(event.component)
		elif event.type == MOVEACTIVATE:
			self._activate(event.component)
		elif event.type == MOVEDEACTIVATE:
			self._deactivate(event.component)

	def update(self, time):
		self.delta = time
		# iterate over active move components
		for comp in [x for x in self.components if x.active]:
			pass
