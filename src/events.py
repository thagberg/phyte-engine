from pygame import USEREVENT

# system events
SYSTEM = USEREVENT + 0
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
ANIMATIONEVENT = USEREVENT + 2
ANIMATIONCOMPLETE = 0
ANIMATIONACTIVATE = 1
ANIMATIONDEACTIVATE = 2

# move events
MOVEEVENT = USEREVENT + 3
MOVECHANGE = 0
MOVERESET = 1
MOVEACTIVATE = 2
MOVEDEACTIVATE = 3

# physics events
PHYSICSEVENT = USEREVENT + 4
ADDFORCE = 0
ADDPHYSICSENTITY = 1
REMOVEPHYSICSCOMPONENT = 2

# input events
INPUTEVENT = USEREVENT + 5
ADDINPUTCOMPONENT = 0
REMOVEINPUTCOMPONENT = 1
UPDATEBINDINGS = 2
ADDINPUTBUFFERCOMPONENT = 3
REMOVEINPUTBUFFERNCOMPONENT = 4
BUFFERINPUT = 5

# graphics events
GRAPHICSEVENT = USEREVENT + 6
ADDGRAPHICSCOMPONENT = 0
REMOVEGRAPHICSCOMPONENT = 1
