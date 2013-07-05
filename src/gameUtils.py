import pygame

MENUEVENT = pygame.USEREVENT + 1
COLLISIONEVENT = pygame.USEREVENT + 2
CHANGEFACEEVENT = pygame.USEREVENT + 3
INPUTEVENT1 = pygame.USEREVENT + 4
INPUTEVENT2 = pygame.USEREVENT + 5

class Binding:
    def __init__(self, key, hold_time=0):
        self.key       = key
        self.hold_time = hold_time


class Inputs:
       
    def __init__(self, bindings=None):
        if bindings == None:
            self.bindings = {
                "up": Binding(pygame.K_UP),
                "down": Binding(pygame.K_DOWN),
                "left": Binding(pygame.K_LEFT),
                "right": Binding(pygame.K_RIGHT),
                "lp": Binding(pygame.K_a),
                "mp": Binding(pygame.K_s),
                "hp": Binding(pygame.K_d),
                "lk": Binding(pygame.K_z),
                "mk": Binding(pygame.K_x),
                "hk": Binding(pygame.K_c),
                "pause": Binding(pygame.K_RETURN)
            }
        else:
            self.bindings = bindings
        
        self.inputState = {"up": False,
                       "down": False,
                       "right": False,
                       "left": False,
                       "lp": False,
                       "mp": False,
                       "hp": False,
                       "lk": False,
                       "mk": False,
                       "hk": False,
                       "pause": False}
        
        self.buffer = InputBuffer()
        
    def lookup_binding(self, key_entered):
        for name, binding in self.bindings.items():
            if key_entered == binding.key:
                return name
        """for binding, key_bound in self.bindings.items():
            if key_entered == key_bound:
                return binding"""
            
        return "not found"
        
    def getInputState(self, events):
        for event in events:
            
            if event.type == pygame.KEYDOWN:
                binding = self.lookup_binding(event.key)
                if binding != "not found":
                    self.bindings[binding].hold_time += 1
                    newInput = Input()
                    newInput.inputName = binding
                    newInput.timeSinceInput = 0
                    self.buffer.push(newInput)
                    self.inputState[binding] = True
                    print "KEYDOWN: %s" % binding
                    
            if event.type == pygame.KEYUP:
                binding = self.lookup_binding(event.key)
                if binding != "not found":
                    self.bindings[binding].hold_time = 0
                    self.inputState[binding] = False
                    print "KEYUP: %s" % binding

        return self.inputState


class InputBuffer:
    
    def __init__(self, expire_time=800):
        self.buffer = list()
        self.expire_time = expire_time

    def expireInputs(self):
        for thisInput in self.buffer:
            if thisInput.timeSinceInput > self.expire_time:
                self.buffer.remove(thisInput)

    def push(self, newInput):
        self.buffer.append(newInput)

    def update_times(self, time_since_last_update):
        for this_input in self.buffer:
            this_input.timeSinceInput += time_since_last_update


class Input:
    
    def __init__(self):
        self.inputName      = ""
        self.timeSinceInput = 0


def getMinTransVect(rect1, rect2):
    mtv = [0, 0]
    shiftLeft = (rect2[0] - (rect1[0] + rect1[2])) + 1
    shiftRight = (rect1[0] - (rect2[0] + rect2[2])) + 1
    shiftUp = (rect2[1] - (rect1[1] + rect1[3])) + 1
    shiftDown = (rect1[1] - (rect2[1] + rect2[3])) + 1
    
    mtv[0] = shiftLeft if (shiftLeft >= shiftRight) else shiftRight
    mtv[1] = shiftUp if (shiftUp >= shiftDown) else shiftDown
    
    return mtv


def get_reverse_crop(surface, rect):
    """Used to get a cropped image from a reversed spritesheet"""
    origin = (surface.get_width(), 0) 
    return pygame.Rect(origin[0] - rect.width - rect.x,
                       rect.y,
                       rect.width,
                       rect.height)


def trans_rect_to_world(rect, parent_loc, reverse=False):
    if reverse:
        trans_rect = pygame.Rect(parent_loc[0] - (rect.x + rect.width),
                                 rect.y + parent_loc[1], rect.width, rect.height)
    else:
        trans_rect = pygame.Rect(rect.x + parent_loc[0], rect.y + parent_loc[1],
                                 rect.width, rect.height)
    return trans_rect


def get_opponent(player_number, players):
    if player_number == 1:
        return players[1]
    else:
        return players[0]


def get_player(player_number, players):
    return players[player_number - 1]

def map_inputs_terminal(player):
    print "Inputs for Player %d" % player.player_number
    bindings = player.inputState.bindings
    for key in bindings:
        print "\tEnter input for: %s" % key
        events = pygame.event.get([pygame.KEYDOWN, pygame.JOYBUTTONDOWN, pygame.JOYAXISMOTION])
        if events[0].type == pygame.KEYDOWN:
            bindings[key] = events[0].key
        elif events[0].type == pygame.JOYBUTTONDOWN:
            bindings[key] = events[0].button
        elif events[0].type == pygame.JOYAXISMOTION:
            bindings[key] = events[0].axis

