from events import *
from pygame import font


class TextComponent(object):
	default_color = (0,0,0)

	def __init__(self, entity_id, text, **style=None):
		self.entity_id = entity_id
		self.text = text
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
	def __init__(self, components=None):
		self.components = list() if components is None else components