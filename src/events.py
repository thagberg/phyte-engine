from pygame import USEREVENT

# system events
UPDATEDIRTY = 0
FREEZE = 1
COLLISION = 2
'''     COLLISION:
            hitter: reference to player owning the hitactive hitbox
            hittee: reference to player owning the hurtactive hitbox
            hitbox: the hitactive hitbox in the collision
            hurtbox: the hurtactive hitbox in the collision
            damage: amount of damage done by the move causing the collision
            hitstun: number of frames of hitstun caused by the move
            stun: amount of stun caused by the move
            push: distance of push the hit causes
'''
CHANGEFACE = 3

# animation events
ANIMATIONEVENT = 4
ANIMATIONCOMPLETE = 5
ANIMATIONACTIVATE = 6
ANIMATIONDEACTIVATE = 7

# move events
MOVEEVENT = 8
MOVECHANGE = 9
MOVERESET = 10
MOVEACTIVATE = 11
MOVEDEACTIVATE = 12

# physics events
PHYSICSEVENT = 13
ADDFORCE = 14
ADDPHYSICSENTITY = 15
REMOVEPHYSICSCOMPONENT = 16

# input events
INPUTEVENT = 17
ADDINPUTCOMPONENT = 18
REMOVEINPUTCOMPONENT = 19
UPDATEBINDINGS = 20
KEYDOWN = 21
KEYUP = 22
JOYBUTTONDOWN = 23
JOYBUTTONUP = 24
MOUSEBUTTONDOWN = 25
MOUSEBUTTONUP = 26
JOYAXISMOTION = 27

# input-buffer events
INPUTBUFFEREVENT = 28
ADDINPUTBUFFERCOMPONENT = 29
REMOVEINPUTBUFFERNCOMPONENT = 30
BUFFERINPUT = 31

# graphics events
GRAPHICSEVENT = 32
ADDGRAPHICSCOMPONENT = 33
REMOVEGRAPHICSCOMPONENT = 34
CHANGECROP = 35
CHANGEDEST = 36
CHANGESURFACE = 37
CHANGEDISPLAY = 38
CHANGEZLEVEL = 39

# text events
TEXTEVENT = 40
ADDTEXTCOMPONENT = 41
REMOVETEXTCOMPONENT = 42
UPDATETEXT = 43

class GameEvent(object):
	def __init__(self, type, **kwargs):
		self.type = type
		for key, value in kwargs.items():
			setattr(self, key, value)
