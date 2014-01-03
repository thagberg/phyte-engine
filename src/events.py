from pygame import USEREVENT

class GameEvent(object):
    def __init__(self, type, **kwargs):
        self.type = type
        for key, value in kwargs.items():
            setattr(self, key, value)


# use this to keep track of the highest event value
__HIGHEVENT = 80 

# system events
UPDATEDIRTY = 0
FREEZE = 1
COLLISION = 2
CHANGEFACE = 3

# animation events
ANIMATIONEVENT = 4
ANIMATIONCOMPLETE = 5
ANIMATIONACTIVATE = 6
ANIMATIONDEACTIVATE = 7
ANIMATIONSTEP = 49
ANIMATIONJUMP = 50
ADDANIMATIONCOMPONENT = 73
REMOVEANIMATIONCOMPONENT = 74

# move events
MOVEEVENT = 8
MOVECHANGE = 9
MOVERESET = 10
MOVEACTIVATE = 11
MOVEDEACTIVATE = 12
ADDMOVECOMPONENT = 60
REMOVEMOVECOMPONENT = 61

# physics events
PHYSICSEVENT = 13
ADDFORCE = 14
ADDPHYSICSCOMPONENT = 15
REMOVEPHYSICSCOMPONENT = 16
ADDPHYSICSCOMPONENTACTIVE = 79
REMOVEPHYSICSCOMPONENTACTIVE = 80
ADDCOLLIDEABLE = 54
REMOVECOLLIDEABLE = 55
SETCOLLIDEABLES = 56
CLEARCOLLIDEABLES = 57

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
REMOVEINPUTBUFFERCOMPONENT = 30
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

# player events
ADDMETERCOMPONENT = 44
REMOVEMETERCOMPONENT = 45
UPDATEMETER = 46
EMPTYMETER = 47
FULLMETER = 48
ADDPLAYERCOMPONENT = 58
REMOVEPLAYERCOMPONENT = 59
FACINGCHANGE = 72

# debug events
ADDDEBUGCOMPONENT = 51
REMOVEDEBUGCOMPONENT = 52
UPDATEDEBUGCOMPONENT = 53

# execution events
ADDEXECUTIONCOMPONENT = 62
REMOVEEXECUTIONCOMPONENT = 63
ACTIVATEEXECUTIONCOMPONENT = 64
DEACTIVATEEXECUTIONCOMPONENT = 65
ADDBUFFEREDEXECUTIONCOMPONENT = 68
REMOVEBUFFEREDEXECUTIONCOMPONENT = 69
ACTIVATEBUFFEREDEXECUTIONCOMPONENT = 70
DEACTIVATEBUFFEREDEXECUTIONCOMPONENT = 71

# state events
ADDSTATECOMPONENT = 66
REMOVESTATECOMPONENT = 67

# movement events
ADDMOVEMENTCOMPONENT = 75
REMOVEMOVEMENTCOMPONENT = 76
ACTIVATEMOVEMENTCOMPONENT = 77
DEACTIVATEMOVEMENTCOMPONENT = 78