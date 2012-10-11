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
        self.secondaryState     = PlayerState.FALLING
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

    
    
    def do_move(self):
        ''' do_move : executes the current move, which includes managing each move frame's hit-boxes and forces'''
        '''if the current move is invalid, find a proper one'''
        if self.current_move > -1:                                           # check for valid move index 
            if self.current_move < len(self.moves):                          #
                currentFrame = self.moves[self.current_move].execute()        
                if currentFrame:                                            # was this a valid move?
                    self.playerBoxes = currentFrame.hitBoxes
                    self.playerForces.append(currentFrame.frameForce)
                    self.imageLoc = currentFrame.animation.image_loc
                    self.cropSize = currentFrame.animation.crop_size
                    if currentFrame.projectile != None:
                        proj_copy = copy.deepcopy(self.projectile_mapping[currentFrame.projectile])
                        proj_copy.hit_box.rect[0] += self.location[0]
                        proj_copy.hit_box.rect[1] += self.location[1]
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
                    self.secondaryState = PlayerState.ATTACKING
                elif self.current_inputs["left"]:
                    self.secondaryState = PlayerState.CROUCHING if self.facing_left else PlayerState.BLOCKING
                elif self.current_inputs["right"]:
                    self.secondaryState = PlayerState.BLOCKING if self.facing_left else PlayerState.CROUCHING
            else:           # player is in one of the standing states
                self.primary_state = PlayerState.STANDING
                if self.attacking:
                    self.secondaryState = PlayerState.ATTACKING
                elif self.current_inputs["left"]:
                    if self.facing_left:
                        self.secondaryState = PlayerState.WALKING
                    else:
                        self.secondaryState = PlayerState.BACKING
                elif self.current_inputs["right"]:
                    if self.facing_left:
                        self.secondaryState = PlayerState.BACKING
                    else:
                        self.secondaryState = PlayerState.WALKING
                else:
                    self.secondaryState = PlayerState.STANDING

            if self.current_inputs["up"]:    # player is in one of the jumping states
                if not(self.attacking):
                    self.primary_state = PlayerState.JUMPING

        else:       # player is either in one of the jumping or falling states
            if self.playerVel[1] > 0:
                self.primary_state = PlayerState.FALLING
            else:
                self.primary_state = PlayerState.JUMPING

            if self.attacking:
                self.secondaryState = PlayerState.ATTACKING
            else:
                self.secondaryState = self.primary_state
            
        # determine if player is attacking now
        if True in (self.current_inputs["lp"], self.current_inputs["mp"], self.current_inputs["hp"],
                    self.current_inputs["lk"], self.current_inputs["mk"], self.current_inputs["hk"]):
            self.secondaryState = PlayerState.ATTACKING
            #self.attacking = True


    
    
    def find_move(self):
        ''' find_move: determine the player's current move'''
        newMove = self.move_mapping["stand"]
        ### check the primary state, then the secondary state to determine the current move ###

        try:
            # standing moves
            if self.primary_state == PlayerState.STANDING:
                if self.secondaryState == PlayerState.ATTACKING:
                    newMove = self.find_move_for_attack()
                else:
                    if self.secondaryState == PlayerState.WALKING:
                        newMove = self.move_mapping["walk"]
                    elif self.secondaryState == PlayerState.BACKING:
                        newMove = self.move_mapping["walk"] # TODO: this should be a backing move
                    elif self.secondaryState == PlayerState.BLOCKING:
                        newMove = self.move_mapping["block"]
                    else:
                        newMove = self.move_mapping["stand"]

            # crouching moves
            elif self.primary_state == PlayerState.CROUCHING:
                if self.secondaryState == PlayerState.ATTACKING:
                    newMove = self.find_move_for_attack()
                else:
                    if self.secondaryState == PlayerState.BLOCKING:
                        newMove = self.move_mapping["block"] #TODO: this should be a crouch-blocking move
                    else:
                        newMove = self.move_mapping["crouch"]

            # jumping moves
            elif self.primary_state == PlayerState.JUMPING:
                if self.secondaryState == PlayerState.ATTACKING:
                    newMove = self.find_move_for_attack()
                else:
                    if self.secondaryState == PlayerState.WALKING:
                        newMove = self.move_mapping["njump"] #TODO: this should be a forwards jump
                    elif self.secondaryState == PlayerState.BACKING:
                        newMove = self.move_mapping["njump"] #TODO: this should be a backward jump
                    else:
                        newMove = self.move_mapping["njump"]

            # falling moves
            elif self.primary_state == PlayerState.FALLING:
                if self.secondaryState == PlayerState.ATTACKING:
                    newMove = self.find_move_for_attack()
                else:
                    newMove = self.move_mapping["fall"]

            # and a catch-all, just in case
            else:
                newMove = self.move_mapping["stand"]

            # now check if attacking
            if self.secondaryState == PlayerState.ATTACKING:
                newMove = self.find_move_for_attack()
                
        except KeyError:
            newMove = 0

        # the new move is found, so change the current move
        self.change_move(newMove)

    

    def orient_boxes(self):
        ''' orient_boxes: hitbox coordinates are relative to the player's location, so their absolute position
        is the sum of their own location and the player's'''
        for box in self.playerBoxes:
            box.rect[0] += self.location[1]
            box.rect[1] += self.location[1]
        
    
            
    def reset_move(self, move):
        ''' reset_move: reset the frames of a move'''
        self.moves[move].reset()
        
    
        
    def change_move(self, newMove):
        ''' change_move: resets the current move and switches to the given one'''
        if newMove != self.current_move:
            self.reset_move(newMove)
            self.current_move = newMove
        
    
        
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
            if self.secondaryState == PlayerState.WALKING:
                self.playerVel[0] = self.walkingSpeed * (-1 if self.facing_left else 1)
            elif self.secondaryState == PlayerState.BACKING:
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
            projectile.hit_box.rect[0] += -projectile.projectile_speed[0] if self.facing_left else projectile.projectile_speed[0]
            projectile.hit_box.rect[1] += projectile.projectile_speed[1]
        
    

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
            elif self.current_inputs["lp"]:
                new_move = self.move_mapping["lp"]

        if (self.moves[new_move].cancel_priority > self.moves[self.current_move].cancel_priority and self.hit_opponent) or not(self.attacking):
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

   
class Move:
    '''encapsulates the frames of a move, as well as the logic for executing the move'''
    
    def __init__(self):
        self.movFrames          = list()
        self.movIndex           = 0
        self.projectile         = False
        self.bufferable         = False
        self.state              = 0
        self.cancel_priority    = 0

    def execute(self):
        if self.movIndex < len(self.movFrames):
            thisFrame = self.movFrames[self.movIndex].execute()
            self.movIndex += 1
            return thisFrame
        else:
            self.movIndex = 0
            return False
    
    def reset(self):
        self.movIndex = 0
   

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
    
    def __init__(self):
        self.rect = [0,0,10,10]
        self.hitActive = False
        self.hurtActive = False


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
        self.projectile_speed   = [10, 0]
        self.hit_box            = HitBox()
        self.animation          = list()


class Animation_Frame:
    '''represents one frame of an animation'''

    def __init__(self):
        self.image_loc          = [0, 0]
        self.crop_size          = [64, 64]
        self.animation_index    = 0         #TODO: decide whether or not I should remove this attribute
