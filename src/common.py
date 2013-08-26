WHITE = ( 255, 255, 255)

class LocationComponent(object):
	def __init__(self, entity_id, point):
		self.entity_id
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