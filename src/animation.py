from system import System
from pygame import event
from events import *

class FrameComponent(object):
	def __init__(self, entity_id, hitboxes=None, force=(0,0), crop=None, 
				 repeat=0, push_box=None):
		self.entity_id = entity_id
		self.hitboxes = list() if hiboxes is None else hitboxes
		self.force = force
		self.crop = crop
		self.repeat = repeat
		self.push_box = push_box
		self.repeat_index = 0


class AnimationComponent(object):
	def __init__(self, entity_id, frames=None, loop=False):
		self.entity_id
		self.frames = list() if frames is None else frames
		self.loop = loop
		self.current_frame = None
		self.current_index = 0

	def reset(self):
		self.current_frame = None
		self.current_index = 0


class CropComponent(object):
	def __init__(self, entity_id, x=0, y=0, w=0, h=0):
		self.entity_id = entity_id
		self.x = x
		self.y = y
		self.w = w
		self.h = h


class AnimationSystem(System):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = list() if components is None else components

	def _add(self, component):
		self.components.append(component)

	def _remove(self, component):
		component.reset()
		try:
			self.components.remove(component)
		except ValueError as e:
			print "Not able to remove component from AnimationSystem: %s" % e.strerror

	def handle_event(self, event):
		if event.type == ANIMATIONCOMPLETE:
			self._remove(event.component)
		elif event.type == ANIMATIONACTIVATE:
			self._add(event.component)
		elif event.type == ANIMATIONDEACTIVATE:
			self._remove(event.component)
	

	def update(self, time, events=None):
		for component in self.components:
			cur_frame = component.current_frame
			# first determine if this frame needs to be repeated
			if cur_frame is not None and cur_frame.repeat > cur_frame.repeat_index:
				cur_frame.repeat_index += 1
			else:
				# test if we need to reset values and move to next frame
				if cur_frame is not None:
					cur_frame.repeat_index = 0
					component.current_index += 1
				# have we gone past the end of this animation?
				if component.current_index >= len(self.frames):
					component.current_index = 0
					if not component.loop:
						cur_frame = None
						new_event = event.Event(ANIMATIONCOMPLETE,
												component=target)
						event.post(new_event)
						continue
				cur_frame = copy.deepcopy(component.frames[component.current_index])
