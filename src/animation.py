import copy
from system import System
from events import *

class FrameComponent(object):
    def __init__(self, entity_id, hitboxes=None, force=(0,0), crop=None, 
                 repeat=0, push_box=None):
        self.entity_id = entity_id
        self.hitboxes = list() if hitboxes is None else hitboxes
        self.force = force
        self.crop = crop
        self.repeat = repeat
        self.push_box = push_box
        self.repeat_index = 0


class AnimationComponent(object):
    def __init__(self, entity_id, frames=None, loop=False, graphic=None):
        self.entity_id = entity_id
        self.frames = list() if frames is None else frames
        self.loop = loop
        self.current_frame = None
        self.current_index = 0
        self.graphic = graphic

    def reset(self):
        self.current_frame = None
        self.current_index = 0


class CropComponent(object):
    def __init__(self, entity_id, x=0, y=0, w=0, h=0):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class AnimationSystem(System):
    def __init__(self, factory, components=None):
        self.factory = factory
        self.components = list() if components is None else components

    def _add(self, component):
        self.components.append(component)
        # crop the graphic component
        c = component
        if c.graphic and c.frames:
            c.current_frame = c.frames[c.current_index]
            c_f = c.current_frame
            cr_event = GameEvent(CHANGECROP, component=c.graphic,
                                 area=c_f.crop)
            self.delegate(cr_event)


    def _remove(self, component):
        component.reset()
        # must fire event to remove grahpics components as well
        if component.graphic:
            rg_event = GameEvent(REMOVEGRAPHICSCOMPONENT, component=component)
            self.delegate(rg_event)
        #TODO: once physics is implemented, will probably want to
        # loop over frames and remove hitboxes components as well
        try:
            self.components.remove(component)
        except ValueError as e:
            print "Not able to remove component from AnimationSystem: %s" % e.strerror

    def _step(self, component):
        '''Step to the next frame within the animation.  Deactivate the 
        animation if we've burned all of the frames, or loop to the beginning
        if this is a looping animation'''
        # repeat the current frame again if necessary
        c = component
        c_f = c.current_frame
        if c_f:
            if c_f.repeat and c_f.repeat_index < c_f.repeat:
                c_f.repeat_index += 1
                return
            # not repeating the current frame
            c_f.repeat_index = 0
        c.current_index += 1
        # check if we have already iterated over each frame
        if c.current_index >= len(c.frames):
            # if this is a looping animation, start over
            if c.loop:
                c.current_index = 0
            # if not a looping animation, we must now reset the animation
            # object and deactivate it
            else:
                self._reset(c)
                de_event = GameEvent(ANIMATIONDEACTIVATE, component=c)
                self.delegate(de_event)
                return          
        c.current_frame = c.frames[c.current_index]
        # if this animation component has a surface, update the crop
        if c.graphic:
            crop_event = GameEvent(CHANGECROP, component=c.graphic, 
                                   area=c_f.crop)
            self.delegate(crop_event)

    def _jump(self, component, count):
        component.current_index += count
        if component.current_index > len(component.frames):
            if component.loop:
                component.current_index = 0 + (component.currend_index - len(component.frames))
            else:
                self._reset(component)
                return
        component.current_frame = component.frames[component.current_index]             

    def handle_event(self, event):
        if event.type == ANIMATIONCOMPLETE:
            self._remove(event.component)
        elif event.type == ANIMATIONACTIVATE:
            print "Activated new animation component"
            self._add(event.component)
        elif event.type == ANIMATIONDEACTIVATE:
            print "Deactivated animation component"
            self._remove(event.component)
        elif event.type == ANIMATIONSTEP:
            self._step(event.component)
    
    def update(self, time, events=None):
        for component in self.components:
            self._step(component)
