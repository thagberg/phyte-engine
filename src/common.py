from pygame import Rect

WHITE = ( 255, 255, 255)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

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


class MovementComponent(object):
	def __init__(self, entity_id, walk_speed=0, back_speed=0, jump_height=0):
		self.entity_id = entity_id
		self.walk_speed = walk_speed
		self.back_speed = back_speed
		self.jump_height = jump_height


class BoxComponent(object):
	def __init__(self, entity_id, loc, dim=[0,0], hitactive=False, hurtactive=False,
				 expired=False, pushactive=False, blockactive=False, damage=0, 
				 stun=0, hitstun=0, push=[0,0]):
		self.entity_id = entity_id
		self.rect = Rect((loc.x, loc.y), (dim[0], dim[1]))
		self.hitactive = hitactive
		self.hurtactive = hurtactive
		self.expired= expired
		self.pushactive = pushactive
		self.blockactive = blockactive
		self.damage = damage
		self.stun = stun
		self.hitstun = hitstun
		self.push = push
