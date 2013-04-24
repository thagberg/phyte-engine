import gameUtils
import copy

# Player class
class Player:

    gravity     = [0, 2]
    friction    = [2, 0]

    def __init__(self):

        # player image attributes
        self.imageLoc           = [0, 0]
        self.cropSize           = [64, 128]
        self.playerImage        = ""

        # player state attributes
        self.primary_state      = PlayerState.FALLING
        self.secondary_state    = PlayerState.FALLING
        self.hit                = False                 # these values are flags which will help determine state/moves
        self.onGround           = False                 #
        self.facing_left        = False
        self.stunned            = False
        self.attacking          = False

        # player stat attributes
        self.walkingSpeed       = 8
        self.backSpeed          = 5
        self.jumpHeight         = 20

        # player input/move attributes
        self.inputState         = gameUtils.Inputs()
        self.move_inputs        = list()
        self.moves              = list()
        self.current_inputs     = dict()
        self.move_mapping       = dict()
        self.current_move       = -1

        # other player attributes
        self.location           = [0,0]
        self.playerBoxes        = list()
        self.playerForces       = list()
        self.playerVel          = [0, 0]
        self.active_projectiles = list()
        self.projectile_mapping = dict()
        self.player_number      = 1
        self.player_name        = "Stick"
        self.hit_opponent       = False

        # handle to opponent
        self.opponent           = None

    
    
    def do_move(self):
        ''' do_move : executes the current move, which includes managing each move frame's hit-boxes and forces'''
        '''if the current move is invalid, find a proper one'''
        if self.current_move > -1:                                           # check for valid move index 
            if self.current_move < len(self.moves):                          #
                currentFrame = self.moves[self.current_move].execute()        
                if currentFrame:                                            # was this a valid move?
                    self.playerBoxes = currentFrame.hitboxes
                    self.playerForces.append(currentFrame.force)
                    self.imageLoc = currentFrame.image_loc
                    self.cropSize = currentFrame.crop_size
                    if currentFrame.projectile != None:
                        proj_copy = copy.deepcopy(self.projectile_mapping[currentFrame.projectile])
                        proj_copy.location[0] += self.location[0]
                        proj_copy.location[1] += self.location[1]
                        proj_copy.moving_left = self.facing_left
                        self.active_projectiles.append(proj_copy)
                else:
                    self.reset_move(self.current_move)                        # nope, find the valid state and move
                    self.attacking = False
                    self.find_state()
                    self.find_move()
                    self.do_move()
            else:
                self.attacking = False
                self.find_state()                                            # invalid move index
                self.find_move()                                             #
                self.do_move()                                               #
        else:                                                           
            self.attacking = False
            self.find_state()
            self.find_move()
            self.do_move()
            
    
                
    def find_state(self):
        ''' find_state : determine the player's current primary and secondary states'''
        if self.onGround:       # player is on the ground
            if self.current_inputs["down"]:  # player is in one of the crouching states
                self.primary_state = PlayerState.CROUCHING
                if self.attacking:
                    self.secondary_state = PlayerState.ATTACKING
                elif self.current_inputs["left"]:
                    self.secondary_state = PlayerState.CROUCHING if self.facing_left else PlayerState.BLOCKING
                elif self.current_inputs["right"]:
                    self.secondary_state = PlayerState.BLOCKING if self.facing_left else PlayerState.CROUCHING
            else:           # player is in one of the standing states
                self.primary_state = PlayerState.STANDING
                if self.attacking:
                    self.secondary_state = PlayerState.ATTACKING
                elif self.current_inputs["left"]:
                    if self.facing_left:
                        self.secondary_state = PlayerState.WALKING
                    else:
                        if self.opponent != None and self.opponent.attacking:
                            self.secondary_state = PlayerState.BLOCKING
                        else:
                            self.secondary_state = PlayerState.BACKING                          
                elif self.current_inputs["right"]:
                    if self.facing_left:
                        if self.opponent != None and self.opponent.attacking:
                            self.secondary_state = PlayerState.BLOCKING
                        else:
                            self.secondary_state = PlayerState.BACKING                            
                    else:
                        self.secondary_state = PlayerState.WALKING
                else:
                    self.secondary_state = PlayerState.STANDING

            if self.current_inputs["up"]:    # player is in one of the jumping states
                if not(self.attacking):
                    self.primary_state = PlayerState.JUMPING

        else:       # player is either in one of the jumping or falling states
            if self.playerVel[1] > 0:
                self.primary_state = PlayerState.FALLING
            else:
                self.primary_state = PlayerState.JUMPING

            if self.attacking:
                self.secondary_state = PlayerState.ATTACKING
            else:
                self.secondary_state = self.primary_state
            
        # determine if player is attacking now
        if True in (self.current_inputs["lp"], self.current_inputs["mp"], self.current_inputs["hp"],
                    self.current_inputs["lk"], self.current_inputs["mk"], self.current_inputs["hk"]):
            self.secondary_state = PlayerState.ATTACKING
            #self.attacking = True
    
    
    def find_move(self):
        ''' find_move: determine the player's current move'''
        new_move = self.move_mapping["stand"]
        ### check the primary state, then the secondary state to determine the current move ###

        try:
            if self.secondary_state == PlayerState.ATTACKING:
                new_move = self.find_move_for_attack()
            else:
                if self.primary_state == PlayerState.STANDING:
                    if self.secondary_state == PlayerState.WALKING:
                        new_move = self.move_mapping["walk"]
                    elif self.secondary_state == PlayerState.BACKING:
                        new_move = self.move_mapping["walk"] # TODO: this should be a backing move
                    elif self.secondary_state == PlayerState.BLOCKING:
                        new_move = self.move_mapping["block"]
                    else:
                        new_move = self.move_mapping["stand"]
                elif self.primary_state == PlayerState.CROUCHING:
                    if self.secondary_state == PlayerState.BLOCKING:
                        new_move = self.move_mapping["crouchblock"] 
                    else:
                        new_move = self.move_mapping["crouch"]
                elif self.primary_state == PlayerState.JUMPING:
                    if self.secondary_state == PlayerState.WALKING:
                        new_move = self.move_mapping["njump"] #TODO: this should be a forwards jump
                    elif self.secondary_state == PlayerState.BACKING:
                        new_move = self.move_mapping["njump"] #TODO: this should be a backward jump
                    else:
                        new_move = self.move_mapping["njump"]
                elif self.primary_state == PlayerState.FALLING:
                    new_move = self.move_mapping["fall"]
                else:
                    new_move = self.move_mapping["stand"]
        except KeyError:
            new_move = 0

        # the new move is found, so change the current move
        self.change_move(new_move)

    

    def orient_boxes(self):
        ''' orient_boxes: hitbox coordinates are relative to the player's location, so their absolute position
        is the sum of their own location and the player's'''
        for box in self.playerBoxes:
            box.rect[0] += self.location[1]
            box.rect[1] += self.location[1]
        
    
            
    def reset_move(self, move):
        ''' reset_move: reset the frames of a move'''
        self.moves[move].reset()
        
    
        
    def change_move(self, new_move):
        ''' change_move: resets the current move and switches to the given one'''
        if new_move != self.current_move:
            self.reset_move(new_move)
            self.current_move = new_move
        
    
        
    def change_state(self, newState):
        self.primary_state = newState
        if newState in (PlayerState.JUMPING, PlayerState.FALLING):
            self.onGround = False
        else:
            self.onGround = True

        if newState == PlayerState.CROUCHING:
            self.crouching = True
        
    
        
    def update(self):

        self.find_state()
        self.find_move()
        self.do_move()

        if not(self.onGround):      # player is in the air
            self.playerForces.append(Player.gravity)
            if self.primary_state == PlayerState.JUMPFORWARD:
                self.playerVel[0] = self.walkingSpeed * (-1 if self.facing_left else 1)
            elif self.primary_state == PlayerState.JUMPBACKWARD:
                self.playerVel[0] = self.backSpeed * (1 if self.facing_left else -1)
        else:                       # player is on the ground
            if self.secondary_state == PlayerState.WALKING:
                self.playerVel[0] = self.walkingSpeed * (-1 if self.facing_left else 1)
            elif self.secondary_state == PlayerState.BACKING:
                self.playerVel[0] = self.backSpeed * (1 if self.facing_left else -1)
            else:
                self.playerVel[0] = 0
            
            # even if secondary state is walking or backing, the player can still be jumping
            if self.primary_state == PlayerState.JUMPING:
                self.playerForces.append([0, -self.jumpHeight])
                self.onGround = False
        
        self.apply_forces()

        self.playerForces = list()

        # move any active_projectiles
        for projectile in self.active_projectiles:
            projectile.location[0] += -projectile.speed[0] if projectile.moving_left else projectile.speed[0]
            projectile.location[1] += projectile.speed[1]
    

    def find_move_for_attack(self):
        '''compare input buffer to move inputs, then check current inputs to find move for attack'''
        # first check for a special move match
        new_move = self.current_move
        special_move_name = self.check_for_move()
        if special_move_name != "no match":
            if self.moves[self.move_mapping[special_move_name]].state == self.primary_state:
                new_move = self.move_mapping[special_move_name]

        # no special move match found, check for a normal
        elif self.primary_state == PlayerState.STANDING:
            if self.current_inputs["hp"]:
			    new_move = self.move_mapping["hp"]
            elif self.current_inputs["hk"]:
                new_move = self.move_mapping["hk"]
            elif self.current_inputs["lp"]:
                new_move = self.move_mapping["lp"]

        # determine if current move can be cancelled
        if (self.moves[new_move] in self.moves[self.current_move].cancellable and self.hit_opponent) or not(self.attacking):
            self.attacking = True
            return new_move
        else:
            return self.current_move


    def apply_forces(self):
        netForce = [0,0]
        for force in self.playerForces:
            netForce[0] += force[0]
            netForce[1] += force[1]

        self.playerVel[0] += netForce[0]
        self.playerVel[1] += netForce[1]

        self.location[0] += self.playerVel[0]
        self.location[1] += self.playerVel[1]
    
    
    def check_for_move(self):
        '''Search the input buffer for combinations which match special moves'''
        # IMPORTANT: move inputs MUST be ordered in descending priority!!!
        #    otherwise the wrong move may be chosen for execution
        for this_move_input in self.move_inputs:
            move_input_index   = 0

            for this_input in self.inputState.buffer.buffer:
                # semi-hacky: if we're looking for "forward" or "backward" we need to
                #   do some special stuff
                if this_move_input.input_order[move_input_index] == "forward":
                    if (self.facing_left and this_input.inputName == "left") or \
                        (not(self.facing_left) and this_input.inputName == "right"):
                        move_input_index += 1

                elif this_move_input.input_order[move_input_index] == "backward":
                    if (self.facing_left and this_input.inputName == "right") or \
                        (not(self.facing_left) and this_input.inputName == "left"):
                        move_input_index += 1

                elif this_move_input.input_order[move_input_index] == this_input.inputName:
                    move_input_index += 1

                if move_input_index >= len(this_move_input.input_order):
                    return this_move_input.move_name
        
        return "no match"

    def get_current_move(self):
        return self.moves[self.current_move]

   
class Move:
    '''encapsulates the frames of a move, as well as the logic for executing the move'''
    
    def __init__(self):
        self.animation          = Animation()
        self.projectile         = False
        self.bufferable         = False
        self.state              = 0
        self.cancellable        = list()

    def execute(self):
        return self.animation.get_next_frame()

    def reset(self):
        self.animation.reset()



class MoveFrame:
    '''represents one frame of animation within a move and its boxes, forces, and images'''
    
    def __init__(self):
        self.hitBoxes = list()
        self.animation = Animation_Frame()
        self.frameForce = [0,0]
        self.projectile = None
    
    def execute(self):
        return self
   

class MoveInput:
    '''describes the order of inputs for a special move and its move index'''

    def __init__(self):
        self.move_name  = ""
        self.input_order = list()


class HitBox:
    '''represents a collideable hitbox'''
    
    def __init__(self, rect=None, hit_active=False, hurt_active=False):
        self.rect = rect
        self.hitActive = hit_active
        self.hurtActive = hurt_active


class PlayerState:
    '''pseudo-enum which contains all of the possible player states'''
    
    STANDING        = 0
    WALKING         = 1
    JUMPING         = 2    
    FALLING         = 3
    EXECUTING       = 4
    CROUCHING       = 5
    LAYING          = 6
    HIT             = 7
    BACKING         = 8
    BLOCKING        = 9
    ATTACKING       = 10
    HITSTUN         = 11
    JUMPFORWARD     = 12
    JUMPBACKWARD    = 13


class Projectile:
    '''encapsulates a Projectile in a move'''

    def __init__(self):
        self.name           = ""
        self.speed          = [0, 0]
        self.moving_left    = False
        self.frames         = list()
        self.location       = [0, 0]
        self.animation      = Animation()
        self.animation.loop = True


class Animation:
    '''includes a list of frames and some helper functions'''

    def __init__(self):
        self.frames = list()
        self.current_frame = None
        self.current_index = 0
        self.loop = False

    def get_next_frame(self):
        if self.current_index >= len(self.frames):
            self.current_index = 0
            if not self.loop:
                return False
        self.current_frame = self.frames[self.current_index]
        self.current_index += 1
        return self.current_frame

    def get_current_frame(self):
        if self.current_frame is None:
            self.current_frame = self.frames[self.current_index]
        return self.current_frame

    def reset(self):
        self.current_index = 0


class Animation_Frame:
    '''represents one frame of an animation'''

    def __init__(self):
        self.hitboxes           = list()
        self.force              = [0, 0]
        self.image_loc          = [0, 0]
        self.crop_size          = [0, 0]
        self.projectile         = None
        self.animation_index    = 0         #TODO: decide whether or not I should remove this attribute

    def execute(self):
        return self
