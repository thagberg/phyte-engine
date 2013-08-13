from events import *
from pygame import display, draw, event, font, image, mask, \
				   PixelArray, sprite, Surface, surfarray, transform


class GraphicsComponent(object):
	def __init__(self, entity_id, surface, area=None, flags=None):
		self.entity_id = entity_id
		self.surface = surface
		self.area = area
		self.flags = flags


class GraphicsSystem(object):
	def __init__(self, surface, components=None):
		self.components = list() if components is None else components
		self.surface = surface
		# dirties is a list of rects covering affected pixels
		self.dirties = list()

	def update(self, time, events=None):
		# clear dirties list
		self.dirties = list()

		# process events
		for event in events:
			if event.type == GRAPHICSEVENT:
				if event.subtype == ADDGRAPHICSCOMPONENT:
					self.components.append(event.component)
				elif event.subtype == REMOVEGRAPHICSCOMPONENT:
					self.components.remove(event.component)

		# update components
		for comp in self.components:
			self._draw_component(self.surface, comp)

		# post a system even holding the dirty rects
		new_event = event.Event(SYSTEM, subtype=UPDATEDIRTY, dirties=self.dirties)
		event.post(new_event)

	def _draw_component(self, draw_to, comp):
		dirty = draw_to.blit(comp.surface, comp.dest, comp.area, comp.flags)
		self.dirties.append(dirty)

