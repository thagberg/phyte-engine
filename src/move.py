from events import *
from pygame import event

class MoveEntity(object):
	def __init__(self, animation=None, inputs=None):
		self.animation = animation
		self.inputs = inputs


class MoveSystem(object):
	def __init__(self, targets=None):
		self.targets = list() if targets is None else targets

	def _add(self, move):
		self.targets.append(move)

	def _remove(self, move):
		try:
			self.targets.remove(move)
		except ValueError as e:
			print "Not able to remove move from MoveSystem: %s" % e.strerror

	def update(self, time, events=None):
		# process events before updating targets
		for event in events:
			if event.type == MOVEACTIVATEEVENT:
				self._add(event.move)
				new_event = event.EVENT(ANIMATIONACTIVATEEVENT,
										animation=event.move.animation)
				event.post(new_event)
			elif event.type == MOVEDEACTIVATEEVENT:
				self._remove(event.move)
				new_event = event.EVENT(ANIMATIONDEACTIVATEEVENT,
										animation=event.move.animation)
				event.post(new_event)
