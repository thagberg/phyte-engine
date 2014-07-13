from pygame import Rect

WHITE = ( 255, 255, 255)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


class Vector2(object):
    def __init__(self, entity_id, vec):
        self.entity_id = entity_id
        self.x = vec[0]
        self.y = vec[1]

    def __str__(self):
        return '[{x}, {y}]'.format(x=self.x, y=self.y)


class LocationComponent(object):
    def __init__(self, entity_id, point):
        self.entity_id = entity_id
        self.x = point[0]
        self.y = point[1]


class VelocityComponent(object):
    def __init__(self, entity_id, vel):
        self.entity_id = entity_id
        self.x = vel[0]
        self.y = vel[1]


class BoxComponent(object):
    def __init__(self, entity_id, rect, hitactive=False, 
                 hurtactive=False, expired=False, solid=False, blockactive=False, 
                 damage=0, stun=0, hitstun=0, push=[0,0], moveable=False):
        self.entity_id = entity_id
        self.rect = rect
        self.hitactive = hitactive
        self.hurtactive = hurtactive
        self.expired = expired
        self.solid = solid 
        self.blockactive = blockactive
        self.damage = damage
        self.stun = stun
        self.hitstun = hitstun
        self.push = push
        self.moveable = moveable 

    def __str__(self):
        return '[{x},{y},{w},{h}] {hi}:{hu}:{so}:{ba}:{st}:{hs}:{mv}'.format(
            x=self.rect.x,
            y=self.rect.y,
            w=self.rect.w,
            h=self.rect.h,
            hi=self.hitactive,
            hu=self.huractive,
            so=self.solid,
            ba=self.blockactive,
            st=self.stun,
            hs=self.hitstun,
            mv=self.moveable)


class AssetComponent(object):
    def __init__(self, file_name, surface):
        self.file_name = file_name
        self.surface = surface
