from ocempgui.widgets import *
from ocempgui.widgets.components import TextListItem

class EditorFrame(TextListItem):
    def __init__(self, renderer, draw_to, offset=(0,0), widgets=None):
        super(EditorFrame, self).__init__()
        self.renderer = renderer
        self.draw_to = draw_to
        self.offset = offset
        self.widgets = widgets if widgets is not None else list()
        self.text = 'Base Frame'

    def activate(self):
        for widget in self.widgets:
            self.renderer.add_widget(widget)

    def deactivate(self):
        for widget in self.widgets:
            self.renderer.remove_widget(widget)

    def set_pos(self, prop, pos):
        off = self.offset
        prop.topleft = (off[0] + pos[0], off[1] + pos[1])

    def update(self, events):
        for event in events:
            pass

