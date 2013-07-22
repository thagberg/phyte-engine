from pygame import event
from events import *

class FrameEntity(object):
	def __init__(self, hitboxes=None, force=(0,0), crop=None, repeat=0,
				 push_box=None):
		self.hitboxes = list() if hiboxes is None else hitboxes
		self.force = force
		self.crop = crop
		self.repeat = repeat
		self.push_box = push_box
		self.repeat_index = 0


class AnimationEntity(object):
	def __init__(self, frames=None, loop=False):
		self.frames = list() if frames is None else frames
		self.loop = loop
		self.current_frame = None
		self.current_index = 0

	def reset(self):
		self.current_frame = None
		self.current_index = 0


class CropEntity(object):
	def __init__(self, x=0, y=0, w=0, h=0):
		self.x = x
		self.y = y
		self.w = w
		self.h = h


class AnimationSystem(object):
	def __init__(self, targets=None):
		self.targets = list() if targets is None else targets

	def _add(self, animation):
		self.targets.append(animation)

	def _remove(self, animation):
		animation.reset()
		try:
			self.targets.remove(animation)
		except ValueError as e:
			print "Not able to remove animation from AnimationSystem: %s" % e.strerror

	def update(self, time, events=None):
		# process events before updating targets
		for event in events:
			if event.type == ANIMATIONCOMPLETEEVENT:
				try:
					self._remove(event.animation)
				except ValueError as e:
					print "Not able to remove animation from AnimationSystem: %s" % e.strerror
			elif event.type == ANIMATIONACTIVATEEVENT:
				self._add(event.animation)
			elif event.type == ANIMATIONDEACTIVATEEVENT:
				self._remove(event.animation)

		for target in targets:
			cur_frame = target.current_frame
			# first determine if this frame needs to be repeated
			if cur_frame is not None and cur_frame.repeat > cur_frame.repeat_index:
				cur_frame.repeat_index += 1
			else:
				# test if we need to reset values and move to next frame
				if cur_frame is not None:
					cur_frame.repeat_index = 0
					target.current_index += 1
				# have we gone past the end of this animation?
				if target.current_index >= len(self.frames):
					target.current_index = 0
					if not target.loop:
						cur_frame = None
						new_event = event.Event(ANIMATIONCOMPLETEEVENT,
												animation=target)
						event.post(new_event)
						continue
				cur_frame = copy.deepcopy(target.frames[target.current_index])
