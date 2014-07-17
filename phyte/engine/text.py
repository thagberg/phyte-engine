import common
from system import System
from events import *
from pygame import font


DEFAULT_COLOR = (0,0,0)


class TextComponent(object):

    def __init__(self, entity_id, text, loc=None, graphic=None, 
                 active=False, style=None):
        self.style = dict() if style is None else style
        self.entity_id = entity_id
        self.text = text
        self.loc = loc
        self.graphic = graphic
        self.active = active
        self.size = style.get('size', 12)
        self.bold = style.get('bold', False)
        self.italic = style.get('italic', False)
        self.underline = style.get('underline', False)
        self.background = style.get('background', None)
        self.aa = style.get('aa', False)
        self.color = style.get('color', DEFAULT_COLOR)
        #self.font = style.get('font', font.SysFont('monospace', self.size, False, False))
        self.font = None
        #self.font.set_underline(self.underline)


class TextSystem(System):
    def __init__(self, factory, components=None):
        self.factory = factory
        self.components = list() if components is None else components

    def _activate(self, component):
        comp = component
        comp.active = True
        # activate graphic component
        new_event = GameEvent(ACTIVATEGRAPHICCOMPONENT, component=comp.graphic)
        self.delegate(new_event)

    def _deactivate(self, component):
        comp = component
        comp.active = False
        # deactivate graphic component
        new_event = GameEvent(DEACTIVATEGRAPHICCOMPONENT, component=comp.graphic)
        self.delegate(new_event)

    def handle_event(self, event):
        if event.type == ADDTEXTCOMPONENT:
            comp = event.component
            print "Added new text component"
            self.components.append(comp)
            # if no font has yet been initialized for this component, do it now
            if not comp.font:
                comp.font = comp.style.get('font', font.SysFont('monospace', comp.size, False, False))
                comp.font.set_underline(comp.underline)
            if not comp.graphic:
                self._update_graphic(comp)
        elif event.type == REMOVETEXTCOMPONENT:
            self.components.remove(ev.component)
        elif event.type == UPDATETEXT:
            event.component.text = event.text
            self._update_graphic(event.component)
        elif event.type == ACTIVATETEXTCOMPONENT:
            self._activate(event.component)
        elif event.type == DEACTIVATETEXTCOMPONENT:
            self._deactivate(event.component)

    def update(self, time):
        self.delta = time
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
                                    surface=new_surf, dest=comp.loc,
                                    active=True)
            comp.graphic = new_comp
