import player
import pygame
import json

def load_character(character_name):
    """search for a .char file with the given character name, then return the parsed .char object"""
    try:
        char_file = open("../content/" + character_name + ".char") 
    except IOError: 
        print("Unable to find .char file for character: " + character_name)

    if char_file is None:
        return "no character found"

    # parse the entire dumped contents of the .char file
    character_config = json.loads(char_file.read())

    return character_config


def create_player(character_config, player_number):
    # first initialize player and organize config data
    this_player     = player.Player()
    character       = character_config["character"]
    name            = character["name"]
    image           = pygame.image.load("../content/" + character["spritesheet"])
    walking_speed   = character["walkingspeed"]
    back_speed      = character["backspeed"]
    jump_height     = character["jumpheight"]
    projectiles     = character["projectiles"]
    moves           = character["moves"]
    movements       = moves["movement"]
    normal_moves    = moves["normals"]
    special_moves   = moves["specials"]
    input_specials  = special_moves["inputspecials"]
    charge_specials = special_moves["chargespecials"]

    this_player.name        = name
    this_player.playerImage = image

    # map projectiles
    for projectile in projectiles:
        new_proj = create_projectile(projectile)
        this_player.projectile_mapping[new_proj.name] = new_proj

    # map movements
    for move_name, move in movements.iteritems():
        this_player.moves.append(create_move(move))
        this_player.move_mapping[move_name] = len(this_player.move_mapping)

    # map normal moves
    for move_name, move in normal_moves.iteritems():
        this_player.moves.append(create_move(move))
        this_player.move_mapping[move_name] = len(this_player.move_mapping)

    # map input special moves
    for move_name, move in input_specials.iteritems():
        this_player.moves.append(create_move(move))
        this_player.move_mapping[move_name] = len(this_player.move_mapping)
        
        if "inputs" in move:
            inputs = move["inputs"]
            this_move_input = player.MoveInput()
            this_move_input.move_name = move_name
            this_move_input.input_order = inputs
            this_player.move_inputs.append(this_move_input)

    # some ugly, hacky stuff we're doing to re-map cancellable lists so that they use the index value
    #   of the move rather than its string name (makes it easier to determine cancels during runtime)
    for move_name, move in this_player.move_mapping.iteritems():
        cancellable_list    = this_player.moves[move].cancellable
        index_list          = list()
        for cancellable in cancellable_list:
            index_list.append(this_player.move_mapping[cancellable])

    return this_player

def create_move(move_config):
    new_move = player.Move()

    frames = move_config["frames"]
    if "state" in move_config:
        new_move.state = move_config["state"]
    if "priority" in move_config:
        new_move.priority = move_config["priority"]
    if "cancellable" in move_config:
        new_move.cancellable = move_config["cancellable"]
    if "frames" in move_config:
        for frame in frames:
            new_frame = create_frame(frame)
            if "repeatcount" in frame:
                for repeat in range(frame["repeatcount"]):
                    new_move.movFrames.append(new_frame) 
    return new_move

def create_projectile(projectile_config):
    new_proj = player.Projectile()
    if "name" in projectile_config:
        new_proj.name = projectile_config["name"]
    if "speed" in projectile_config:
        new_proj.speed = projectile_config["speed"]
    if "frames" in projectile_config:
        for frame in projectile_config["frames"]:
            new_frame = create_frame(frame)
            if "repeatcount" in frame:
                for repeat in range(frame["repeatcount"]):
                    new_proj.animation.frames.append(new_frame)
    return new_proj

def create_frame(frame_config):
    new_frame = player.Animation_Frame()
    if "force" in frame_config:
        new_frame.force = frame_config["force"]
    if "imagecrop" in frame_config:
        new_frame.image_loc = frame_config["imagecrop"]
    if "cropsize" in frame_config:
        new_frame.crop_size = frame_config["cropsize"]
    if "projectile" in frame_config and frame_config["projectile"] != False:
        new_frame.projectile = frame_config["projectile"]
    if "hitboxes" in frame_config:
        for hitbox in frame_config["hitboxes"]:
            new_frame.hitboxes.append(create_hitbox(hitbox))
    return new_frame

def create_hitbox(hitbox_config):
    new_hitbox = player.HitBox()
    if "rect" in hitbox_config:
        new_hitbox.rect = hitbox_config["rect"]
    if "hitActive" in hitbox_config:
        new_hitbox.hitActive = hitbox_config["hitActive"]
    if "hurtActive" in hitbox_config:
        new_hitbox.hurtActive = hitbox_config["hurtActive"]
    return new_hitbox