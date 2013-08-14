from events import *
from pygame import display, draw, event, font, image, mask, \
				   PixelArray, sprite, Surface, surfarray, transform

#TODO: add events for crop update to graphics, for use with animation system

class GraphicsComponent(object):
	def __init__(self, entity_id, surface, dest=None, area=None, flags=None,
				 z_level=0):
		self.entity_id = entity_id
		self.surface = surface
		self.dest = dest
		self.area = area
		self.flags = flags
		self.z_level = z_level


class TextGraphicsComponent(GraphicsComponent):
	default_color = ( 0, 0, 0)

	def __init__(self, entity_id, text, dest=None, area=None, flags=None, 
			     z_level=0, **style=None):
		# render a font surface
		self.text = text
		self.size = 12 if not 'size' in style else style['size']
		self.bold = False if not 'bold' in style else style['bold']
		self.italic = False if not 'italic' in style else style['italic']
		self.underlind = False if not 'underline' in style else style['underline']
		self.background = None if not 'background' in style else style['background']
		self.aa = False if not 'aa' in stle else style['aa']
		if not 'color' in style:
			self.color = TextGraphicsComponent.default_color
		else:
			self.color = style['color']
		if not 'font' in style['font']:
			self.font = font.SysFont('monospace', self.size, False, False)
		else:
			self.font = style['font']
		self.font.set_underline(self.underline)
		surface = self.font.render(self.text, self.aa, self.color, self.background)

		# now create a graphics component out of the rendered text
		super(TextGraphicsComponent, self).__init__(entity_id, surface, dest,
													area, flags, z_level)


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
					self.components.sort(key=lambda x: x.z_level)
				elif event.subtype == REMOVEGRAPHICSCOMPONENT:
					self.components.remove(event.component)
					self.components.sort(key=lambda x: x.z_level)
				elif event.subtype == CHANGECROP:
					event.component.area = event.area
				elif event.subtype == CHANGEDEST:
					event.component.dest = event.dest
				elif event.subtype == CHANGESURFACE:
					event.component.surface = event.surface
				elif event.subtype == CHANGEDISPLAY:
					self.surface = event.surface
				elif event.subtype == CHANGEZLEVEL:
					event.component.z_level = event.z_level
					self.components.sort(key=lambda x: x.z_level)

		# update components
		for comp in self.components:
			self._draw_component(self.surface, comp)

		# post a system even holding the dirty rects
		new_event = event.Event(SYSTEM, subtype=UPDATEDIRTY, dirties=self.dirties)
		event.post(new_event)

	def _draw_component(self, draw_to, comp):
		dirty = draw_to.blit(comp.surface, comp.dest, comp.area, comp.flags)
		self.dirties.append(dirty)

