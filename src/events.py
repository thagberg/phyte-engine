from pygame import USEREVENT

COLLISION = USEREVENT + 1
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
CHANGEFACE = USEREVENT + 3
FREEZE = USEREVENT + 4
ANIMATIONCOMPLETE = USEREVENT + 5
MOVECHANGE = USEREVENT + 6
MOVERESET = USEREVENT + 7
MOVEACTIVATE = USEREVENT + 8
MOVEDEACTIVATE = USEREVENT + 9
ANIMATIONACTIVATE = USEREVENT + 10
ANIMATIONDEACTIVATE = USEREVENT + 11
ADDFORCE = USEREVENT + 12
ADDPHYSICSENTITY = USEREVENT + 13
REMOVEPHYSICSCOMPONENT = USEREVENT + 14
ADDINPUTCOMPONENT = USEREVENT + 15
REMOVEINPUTCOMPONENT = USEREVENT + 16
UPDATEBINDINGS = USEREVENT + 17
ADDINPUTBUFFERCOMPONENT = USEREVENT + 18
REMOVEINPUTBUFFERNCOMPONENT = USEREVENT + 19
BUFFERINPUT = USEREVENT + 20
