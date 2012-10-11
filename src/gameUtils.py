import pygame

class Inputs:
       
    def __init__(self):
        self.bindings = {"up": pygame.K_UP,
                         "down":  pygame.K_DOWN,
                         "left":  pygame.K_LEFT,
                         "right":   pygame.K_RIGHT,
                         "lp":  pygame.K_a,
                         "mp":  pygame.K_s,
                         "hp":  pygame.K_d,
                         "lk":  pygame.K_z,
                         "mk":  pygame.K_x,
                         "hk":  pygame.K_c,
                         "pause":   pygame.K_RETURN}
        
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
    
    #/ END Input.getInputState
        
#/ END Input class


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
