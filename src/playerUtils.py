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
        this_projectile = player.Projectile()
        this_animation  = player.Animation_Frame()
        this_projectile.projectile_speed    = projectile["speed"]
        this_projectile.hitboxes            = projectile["hitbox"]
        this_animation.image_loc    = projectile["imagecrop"]
        this_animation.crop_size    = projectile["cropsize"]
        this_projectile.animation.append(this_animation)
        this_player.projectile_mapping[projectile["name"]] = this_projectile

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
    this_move = player.Move()

    frames = move_config["frames"]
    if "state" in move_config:
        this_move.state = move_config["state"]
    if "priority" in move_config:
        this_move.priority = move_config["priority"]
    if "cancellable" in move_config:
        this_move.cancellable = move_config["cancellable"]
    for frame in frames:
        this_frame = player.MoveFrame()
        this_frame.animation.image_loc = frame["imagecrop"]
        this_frame.animation.crop_size = frame["cropsize"]
        this_frame.force    = frame["force"]
        if frame["projectile"]:
            this_frame.projectile = frame["projectile"]
        hit_boxes = frame["hitboxes"]
        for hit_box in hit_boxes:
            this_frame.hitBoxes.append(hit_box)
        for repeat in range(frame["repeatcount"]):
            this_move.movFrames.append(this_frame)

    return this_move
