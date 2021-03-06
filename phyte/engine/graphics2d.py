from system import System
from events import *


class GraphicsComponent(object):
    def __init__(self, entity_id, surface, file_name=None, dest=None, area=None, 
                 flags=None, active=False, z_level=0):
        self.entity_id = entity_id
        self.surface = surface
        self.file_name = file_name
        self.dest = dest
        self.area = area
        self.flags = flags
        self.z_level = z_level
        self.active = active


class GraphicsSystem(System):
    def __init__(self, surface, factory, components=None):
        super(GraphicsSystem, self).__init__()
        self.factory = factory
        self.components = list() if components is None else components
        self.surface = surface
        # dirties is a list of rects covering affected pixels
        self.dirties = list()

    def _activate(self, component):
        component.active = True

    def _deactivate(self, component):
        component.active = False

    def handle_event(self, event):  
        if event.type == ADDGRAPHICSCOMPONENT:
            print "Added new graphic component: %s" % event.component
            self.components.append(event.component)
            self.components.sort(key=lambda x: x.z_level)
        elif event.type == REMOVEGRAPHICSCOMPONENT:
            try:
                self.components.remove(event.component)
                self.components.sort(key=lambda x: x.z_level)
            except ValueError, e:
                pass
            print "Removed graphic component: %s" % event.component
        elif event.type == CHANGECROP:
            event.component.area = event.area
        elif event.type == CHANGEDEST:
            event.component.dest = event.dest
        elif event.type == CHANGESURFACE:
            event.component.surface = event.surface
        elif event.type == CHANGEDISPLAY:
            self.surface = event.surface
        elif event.type == CHANGEZLEVEL:
            event.component.z_level = event.z_level
            self.components.sort(key=lambda x: x.z_level)
        elif event.type == ACTIVATEGRAPHICSCOMPONENT:
            self._activate(event.component)
        elif event.type == DEACTIVATEGRAPHICSCOMPONENT:
            self._deactivate(event.component)

    def update(self, time):
        self.delta = time
        # clear dirties list
        self.dirties = list()
        
        # update components
        for comp in [x for x in self.components if x.active]:
            self._draw_component(self.surface, comp)

        # post a system event holding the dirty rects
        new_event = GameEvent(UPDATEDIRTY, dirties=self.dirties)
        self.delegate(new_event)

    def _draw_component(self, draw_to, comp):
        flags = comp.flags if comp.flags else 0
        area = comp.area if comp.area else None
        dest = comp.dest
        dirty = draw_to.blit(comp.surface, 
                             (dest.body.x, dest.body.y), 
                             area, 
                             flags)
        self.dirties.append(dirty)

