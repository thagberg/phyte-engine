from pygame import draw, Rect

import common
from system import System
from events import *


class DebugComponent(object):
    def __init__(self, entity_id, text=None, get_value=None, 
                 rect=None, line=None, ellipse=None, circle=None, 
                 active=False, arc=None, style=None):
        self.style = dict() if style is None else style
        self.entity_id = entity_id
        self.text = text
        self.get_value = get_value
        self.rect = rect
        self.line = line
        self.ellipse = ellipse
        self.circle = circle
        self.arc = arc
        self.active = active
        self.last_value = None


class DebugSystem(System):
    '''System for managing debug artifacts, which can include debug text
    or lines and shapes to be drawn to the screen'''
    def __init__(self, surface, factory, components=None):
        self.surface = surface
        self.factory = factory
        self.components = list() if components is None else components

    def _add(self, component):
        self.components.append(component)

    def _remove(self, component):
        # remove sub-components at the same time (text or graphics)
        if component.text:
            t_event = GameEvent(REMOVETEXTCOMPONENT, component=component.value)
            self.delegate(t_event)
        try:
            self.components.remove(component)
        except ValueError as e:
            print "Not able to remove component from DebugSystem: %s" %e.strerror

    def _update_debug(self, component):
        if component.text:
            t_event = GameEvent(UPDATETEXT, 
                                component=component, 
                                text=component.text)
            self.delegate(t_event)

    def _activate(self, component):
        comp = component
        comp.active = True
        # if this debug component has a rendered text object,
        # we need to activate that too
        if comp.text:
            new_event = GameEvent(ACTIVATETEXTCOMPONENT, component=comp.text)
            self.delegate(new_event)

    def _deactivate(self, component):
        comp = component
        comp.active = False
        # deactivate any rendered text objects as well
        if comp.text:
            new_event = GameEvent(DEACTIVATETEXTCOMPONENT, component=comp.text)
            self.delegate(new_event)

    def handle_event(self, event):
        if event.type == ADDDEBUGCOMPONENT:
            print "Added debug component"
            self._add(event.component)
        elif event.type == REMOVEDEBUGCOMPONENT:
            print "Removing debug component"
            self._remove(event.component)
        elif event.type == UPDATEDEBUGCOMPONENT:
            print "Updating debug component"
            self._update_debug(event.component)
        elif event.type == ACTIVATEDEBUGCOMPONENT:
            self._activate(event.component)
        elif event.type == DEACTIVATEDEBUGCOMPONENT:
            self._deactivate(event.component)

    def update(self, time):
        self.delta = time
        for comp in [x for x in self.components if x.active]:
            # prepare style options
            color = comp.style.get('color', common.BLACK)
            width = comp.style.get('width', 1)

            # draw debug objects
            if comp.rect:
                from pdb import set_trace
                set_trace()
                trans_rect = Rect(comp.rect.rect.x + comp.rect.anchor.body.x,
                                  comp.rect.rect.y + comp.rect.anchor.body.y,
                                  comp.rect.rect.w,
                                  comp.rect.rect.h)
                draw.rect(self.surface, color, trans_rect, width)
            if comp.circle:
                draw.circle(self.surface, color, comp.circle.pos,
                            comp.circle.radius, width)
            if comp.ellipse:
                draw.ellipse(self.surface, color, comp.ellipse.rect,
                             width)
            if comp.arc:
                draw.arc(self.surface, color, comp.arc.start,
                         comp.arc.end, width)
            if comp.line:
                draw.line(self.surface, color, comp.line.closed,
                          comp.line.points, width)

            if comp.get_value:
                text_val = str(comp.get_value())
                if text_val != comp.last_value:
                    # fire event to update rendered graphic for this
                    comp.last_value = text_val
                    tu_event = GameEvent(UPDATETEXT, component=comp.text,
                                         text=text_val)
                    self.delegate(tu_event)
