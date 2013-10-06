from system import System
from events import *

class PhysicsComponent(object):
	def __init__(self, entity_id, box=None, collideables=None):
		self.entity_id = entity_id
		self.box = box 
		self.collideables = list() if not collideables else collideables
		self.forces = list()
		self.pulses = list()


class PhysicsSystem(System):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = list() if components is None else components

	def _add(self, component):
		self.components.add(component)

	def _remove(self, component):
		try:
			self.components.remove(component)
		except ValueError as e:
			print "Error when attempting to remove component from PhysicsManager: %s" % e.strerror

	def handle_event(self, event):
		if event.type == ADDPHYSICSCOMPONENT:
			self._add(event.component)
		elif event.type == REMOVEPHYSICSCOMPONENT:
			self._remove(event.component)
		elif event.type == ADDFORCE:
			event.component.forces.append(event.force)
		elif event.type == ADDCOLLIDEABLE:
			event.component.collideables.append(event.collideable)
		elif event.type == REMOVECOLLIDEABLE:
			try:
				event.component.collideables.remove(event.collideable)
			except ValueError, e:
				print "Cannot remove collideable from PhysicsComponent: %s" % e.strerror
		elif event.type == SETCOLLIDEABLES:
			event.component.collideables = event.collideables
		elif event.type == CLEARCOLLIDEABLES:
			event.component.collideables = list()

	def get_min_trans_vect(self, rect1, rect2):
		mtv = [0, 0]
		shift_left = (rect2[0] - (rect1[0] + rect1[2])) + 1
		shift_right = (rect1[0] - (rect2[0] + rect2[2])) + 1
		shift_up = (rect2[1] - (rect1[1] + rect1[3])) + 1
		shift_down = (rect[1] - (rect2[1] +rect2[3])) + 1

		mtv[0] = shift_left if shift_Left >= shift_right else shift_right
		mtv[1] = shift_up if shift_up >= shift_down else shift_down
		return mtv

	def update(self, time, events=None):
		for comp in self.component:
			comp_rect = comp.box.rect
			coll_rects = [x.box.rect for x in comp.collideables]
			# find the indices of collisions
			collisions = comp_rect.collidelistall(coll_rects)
			# process each collision
			for coll_ind in collisions:
				coll_rect = coll_rects[coll_ind]
				mtv = self.get_min_trans_vect(comp_rect, coll_rect)
				c_event = GameEvent(COLLISION, box1=comp.box,
									box2=comp.collideables[coll_ind].box, 
									mtv=mtv)
				self.delegate(c_event)
