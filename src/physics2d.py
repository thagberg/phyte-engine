from system import System
from events import *

class PhysicsComponent(object):
	def __init__(self, entity_id, body=None):
		self.entity_id = entity_id
		self.body = body
		self.forces = list()


class PhysicsSystem(System):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = list() if components is None else components

	def handle_event(self, event):
		if event.type == ADDPHYSICSCOMPONENT:
			self._add(event.component)
		elif event.type == REMOVEPHYSICSCOMPONENT:
			self._remove(event.component)
		elif event.type == ADDFORCE:
			event.component.forces.append(event.force)

	def update(self, time, events=None):
		for comp in self.component:
			body = comp.body
			forces = comp.forces
			net = [0, 0]
			for force in forces:
				net[0] += force[0]
				net[1] += force[1]
			body.x += net.x
			body.y += net.y

	def _add(self, component):
		self.components.add(component)

	def _remove(self, component):
		try:
			self.components.remove(component)
		except ValueError as e:
			print "Error when attempting to remove component from PhysicsManager: %s" % e.strerror
