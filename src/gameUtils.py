import pygame

MENUEVENT = pygame.USEREVENT + 1
COLLISIONEVENT = pygame.USEREVENT + 2
CHANGEFACEEVENT = pygame.USEREVENT + 3

class Inputs:
       
    def __init__(self):
        self.bindings = {"up":  pygame.K_UP,
                         "down":  pygame.K_DOWN,
                         "left":  pygame.K_LEFT,
                         "right":   pygame.K_RIGHT,
                         "lp":  pygame.K_a,
                         "mp":  pygame.K_s,
                         "hp":  pygame.K_d,
                         "lk":  pygame.K_z,
                         "mk":  pygame.K_x,
                         "hk":  pygame.K_c,
                         "pause":  pygame.K_RETURN}
        
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
        
    def lookupBinding(self, keyEntered):
        for binding, keyBound in self.bindings.items():
            if keyEntered == keyBound:
                return binding
            
        return "not found"
        
    def getInputState(self, events):
        for event in events:
            
            if event.type == pygame.KEYDOWN:
                binding = self.lookupBinding(event.key)
                if binding != "not found":
                    newInput = Input()
                    newInput.inputName = binding
                    newInput.timeSinceInput = 0
                    self.buffer.push(newInput)
                    self.inputState[binding] = True
                    
            if event.type == pygame.KEYUP:
                binding = self.lookupBinding(event.key)
                if binding != "not found":
                    self.inputState[binding] = False
                    
        return self.inputState


class InputBuffer:
    
    def __init__(self):
        self.buffer = list()

    def expireInputs(self):
        for thisInput in self.buffer:
            if thisInput.timeSinceInput > 800:
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