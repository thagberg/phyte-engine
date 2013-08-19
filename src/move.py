from events import *
from pygame import event

class MoveComponent(object):
	def __init__(self, entity_id, animation=None, inputs=None):
		self.entity_id = entity_id
		self.animation = animation
		self.inputs = inputs


class MoveSystem(object):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = list() if components is None else components

	def _add(self, component):
		self.components.append(component)

	def _remove(self, component):
		try:
			self.components.remove(move)
		except ValueError as e:
			print "Not able to remove component from MoveSystem: %s" % e.strerror

	def update(self, time, events=None):
		# process events before updating targets
		for event in events:
			if event.type == MOVEACTIVATE:
				self._add(event.component)
				new_event = event.EVENT(ANIMATIONACTIVATE,
										animation=event.component.animation)
				event.post(new_event)
			elif event.type == MOVEDEACTIVATE:
				self._remove(event.component)
				new_event = event.EVENT(ANIMATIONDEACTIVATE,
										animation=event.component.animation)
				event.post(new_event)
