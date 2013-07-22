from events import *

class PhysicsEntity(object):
	def __init__(self, body=None):
		self.body = body
		self.forces = list()

class HitboxEntity(object):
	def __init__(self, rect=None, hit_active=False, hurt_active=False,
				 push_active=False, expired=False, damage=0, stun=0,
				 hitstun=0, push=(0,0)):
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
	def __init__(self, entities=None):
		self.entities = list() if entities is None else entities

	def update(self, time, events=None):
		for event in events:
			if event.type == ADDFORCEEVENT:
				self.entities[event.id].forces.append(event.force)
			elif event.type == ADDPHYSICSENTITYEVENT:
				self._add(event.entity)
			elif event.type == REMOVEPHYSICSENTITYEVENT:
				self._remove(event.entity)

		for entity in entities:
			body = entity.body
			forces = entity.forces
			net = [0, 0]
			for force in forces:
				net[0] += force[0]
				net[1] += force[1]
			body.x += net.x
			body.y += net.y

	def _add(self, entity):
		self.entities.add(entity)

	def _remove(self, entity):
		try:
			self.entities.remove(entity)
		except ValueError as e:
			print "Error when attempting to remove entity from PhysicsManager: %s" % e.strerror
