from pygame import USEREVENT

COLLISIONEVENT = USEREVENT + 1
'''     COLLISIONEVENT:
            hitter: reference to player owning the hitactive hitbox
            hittee: reference to player owning the hurtactive hitbox
            hitbox: the hitactive hitbox in the collision
            hurtbox: the hurtactive hitbox in the collision
            damage: amount of damage done by the move causing the collision
            hitstun: number of frames of hitstun caused by the move
            stun: amount of stun caused by the move
            push: distance of push the hit causes
'''
CHANGEFACEEVENT = USEREVENT + 3
FREEZEEVENT = USEREVENT + 4
ANIMATIONCOMPLETEEVENT = USEREVENT + 5
MOVECHANGEEVENT = USEREVENT + 6
MOVERESETEVENT = USEREVENT + 7
MOVEACTIVATEEVENT = USEREVENT + 8
MOVEDEACTIVATEEVENT = USEREVENT + 9
ANIMATIONACTIVATEEVENT = USEREVENT + 10
ANIMATIONDEACTIVATEEVENT = USEREVENT + 11
ADDFORCEEVENT = USEREVENT + 12
ADDPHYSICSENTITYEVENT = USEREVENT + 13
REMOVEPHYSICSENTITYEVENT = USEREVENT + 14