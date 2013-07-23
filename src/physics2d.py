from events import *

class PhysicsComponent(object):
	def __init__(self, entity_id, body=None):
		self.entity_id = entity_id
		self.body = body
		self.forces = list()

class HitboxComponent(object):
	def __init__(self, entity_id, rect=None, hit_active=False, 
				 hurt_active=False, push_active=False, expired=False, 
				 damage=0, stun=0, hitstun=0, push=(0,0)):
		self.entity_id = entity_id
		self.rect = rect
		self.hit_active = hit_active
		self.hurt_active = hurt_active
		self.push_active = push_active
		self.expired = expired
		self.damage = damage
		self.stun = stun
		self.hitstun = hitstun
		self.push = push


class PhysicsSystem(object):
	def __init__(self, components=None):
		self.components = list() if components is None else components

	def update(self, time, events=None):
		for event in events:
			if event.type == ADDFORCE:
				self.components[event.id].forces.append(event.force)
			elif event.type == ADDPHYSICSCOMPONENT:
				self._add(event.component)
			elif event.type == REMOVEPHYSICSCOMPONENT:
				self._remove(event.component)

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
