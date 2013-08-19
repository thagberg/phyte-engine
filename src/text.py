from events import *
from pygame import font


class TextComponent(object):
	default_color = (0,0,0)

	def __init__(self, entity_id, text, **style, graphic=None):
		self.entity_id = entity_id
		self.text = text
		self.graphic = graphic
		self.size = 12 if not 'size' in style else style['size']
		self.bold = False if not 'bold' in style else style['bold']
		self.italic = False if not 'italic' in style else style['italic']
		self.underline = False if not 'underline' in style else style['underline']
		self.background = None if not 'background' in style else style['background']
		self.aa = False if not 'aa' in stle else style['aa']
		if not 'color' in style:
			self.color = TextComponent.default_color
		else:
			self.color = style['color']
		if not 'font' in style['font']:
			self.font = font.SysFont('monospace', self.size, False, False)
		else:
			self.font = style['font']
		self.font.set_underline(self.underline)


class TextSystem(object):
	def __init__(self, factory, components=None):
		self.factory = factory
		self.components = list() if components is None else components

	def update(self, time, events=None):
		# process events
		for event in events:	
			if event.u_type == TEXTEVENT:
				if event.subtype == ADDTEXTCOMPONENT:
					self.components.append(event.component)
				elif event.subtype == REMOVETEXTCOMPONENT:
					self.components.remove(event.component)
				elif event.subtype == UPDATETEXT:
					event.component.text = event.text
					self.update_graphic(event.component)

	def _update_graphic(self, comp):
		old_surf = comp.graphic
		new_surf = comp.font.render(comp.text, comp.aa, comp.color, comp.background)
		comp.graphic = new_surf
		rem_event = event.Event(GRAPHICSEVENT, subtype=REMOVEGRAPHICSCOMPONENT,
								component=old_surf)
		add_event = event.EVENT(GRAPHICSEVENT, subtype=ADDGRAPHICSCOMPONENT,
								component=new_surf)
		event.post(rem_event)
		event.post(add_event)
