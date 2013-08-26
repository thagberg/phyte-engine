from system import System
from events import *

class HealthComponent(object):
	def __init__(self, entity_id, health=0):
		self.health = health


class HealthSystem(System):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = dict() if components is None else components

	def handle_event(self, event):
		if event.type == ADDHEALTHCOMPONENT:
			self.components[event.entity_id] = event.component
		elif event.type == REMOVEHEALTHCOMPONENT:
			try:
				del self.components[event.entity_id]
			except KeyError, e:
				print "Cannot remove component from health system: %d" % event.entity_id
		elif event.type == UPDATEHEALTH:
			h_comp = self.components[event.entity_id]
			h_comp.health += event.change
			if h_comp.health <= 0:
				new_event = GameEvent(NOHEALTH, entity_id=event.entity_id,
									  component=h_comp)
				self.delegate(new_event)

