import common
from system import System
from events import *
from pygame import draw


class DebugComponent(object):
    def __init__(self, entity_id, text=None, rect=None, line=None, 
                 ellipse=None, circle=None, arc=None, **style):
        self.entity_id = entity_id
        self.text = text
        self.rect = rect
        self.line = line
        self.ellipse = ellipse
        self.circle = circle
        self.arc = arc
        self.style = style


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
            t_event = GameEvent(REMOVETEXTCOMPONENT, component=component.text)
            self.delegate(t_event)
        try:
            self.components.remove(component)
        except ValueError as e:
            print "Not able to remove component from DebugSystem: %s" %e.strerror

    def _update_debug(self, component):
        if component.text:
            t_event = GameEvent(UPDATETEXT, component.text)

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

    def update(self, time):
        self.delta = time
        for comp in self.components:
            # prepare style options
            if 'color' in comp.style:
                color = comp.style['color']
            else:
                color = common.BLACK
            if 'width' in comp.style:
                width = comp.style['width']
            else:
                width = 1

            # draw debug objects
            if comp.rect:
                draw.rect(self.surface, color, comp.rect, width)
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