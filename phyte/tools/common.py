from ocempgui.widgets.components import TextListItem


WHITE = (255, 255, 255, 255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
PURPLE = (255, 0, 255, 255)
YELLOW = (255, 255, 0, 255)
BLACK = (0, 0, 0, 255)
TRANS = (0, 0, 0, 0)
GRAY = (225, 225, 225, 255)

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

ENTITY_ID = -1


class Component(TextListItem):
    def __init__(self, component, get_text):
        super(Component, self).__init__()
        self.component = component
        self.type_name = self.component.__class__.__name__
        self.get_text = get_text
        self.text = ''
        self.refresh_text()

    def refresh_text(self):
        self.text = self.get_text()
