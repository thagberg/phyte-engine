import common
from system import System
from events import *
from pygame import font


class TextComponent(object):
	default_color = (0,0,0)

	def __init__(self, entity_id, text, loc=None, graphic=None, **style):
		self.entity_id = entity_id
		self.text = text
		self.loc = loc
		self.graphic = graphic
		self.size = 12 if not 'size' in style else style['size']
		self.bold = False if not 'bold' in style else style['bold']
		self.italic = False if not 'italic' in style else style['italic']
		self.underline = False if not 'underline' in style else style['underline']
		self.background = None if not 'background' in style else style['background']
		self.aa = False if not 'aa' in style else style['aa']
		if not 'color' in style:
			self.color = TextComponent.default_color
		else:
			self.color = style['color']
		if not 'font' in style:
			self.font = font.SysFont('monospace', self.size, False, False)
		else:
			self.font = style['font']
		self.font.set_underline(self.underline)


class TextSystem(System):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = list() if components is None else components

	def handle_event(self, event):
		if event.type == ADDTEXTCOMPONENT:
			print "Added new text component"
			self.components.append(event.component)
			if not event.component.graphic:
				self._update_graphic(event.component)
		elif event.type == REMOVETEXTCOMPONENT:
			self.components.remove(ev.component)
		elif event.type == UPDATETEXT:
			event.component.text = event.text
			self._update_graphic(event.component)

	def update(self, time):
		pass

	def _update_graphic(self, comp):
		if comp.background:
			new_surf = comp.font.render(comp.text, comp.aa, comp.color, comp.background)
		else:
			new_surf = comp.font.render(comp.text, comp.aa, comp.color)

		if comp.graphic:
			# if this TextComponent previously had a graphics component reference
			upd_event = GameEvent(CHANGESURFACE, component=comp.graphic, 
								  surface=new_surf)
			self.delegate(upd_event)
		else:
			# there was not previously a graphics component for this TextComponent
			create_comp = self.factory.create_component
			new_comp = create_comp('graphics', entity_id=comp.entity_id,
									surface=new_surf, dest=comp.loc)
			comp.graphic = new_comp
