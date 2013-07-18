#!/usr/bin/python

import pygame
import player
import gameUtils
import playerUtils
import pymenu
import copy

pygame.init()

# Define colors
black  = (   0,   0,   0)
white  = ( 255, 255, 255)
red    = ( 255,   0,   0)
green  = (   0, 255,   0)
blue   = (   0,   0, 255)
yellow = ( 255, 255,   0)
purple = ( 255,   0, 255)
trans  = (   0, 253, 255)

# game state stuff
debug = True
debugFont = pygame.font.SysFont("monospace", 15, False, False)
current_time = pygame.time.get_ticks()
time_since_last_udate = 0
draw_hitboxes = True

# Screen stuffs
size = [700,500]
screen = pygame.display.set_mode(size)
screen.set_alpha(None)
screen.set_colorkey((    0, 255, 255))
pygame.display.set_caption("Bam it's a game")

# Initialize the stage
ground = pygame.Rect(0, 450, size[0], 50)

# Initialize first player
player1_config = playerUtils.load_character("stick")
player1 = playerUtils.create_player(player1_config, 1)
player1.inputState = gameUtils.Inputs()
player1.location = [0, 300]

# Initialize second player
player2_config = playerUtils.load_character("stick")
player2 = playerUtils.create_player(player2_config, 2)
player2.inputState = gameUtils.Inputs(
    bindings={
        "up": gameUtils.Binding(pygame.K_KP8),
        "down": gameUtils.Binding(pygame.K_KP2),
        "left": gameUtils.Binding(pygame.K_KP4),
        "right": gameUtils.Binding(pygame.K_KP6),
        "lp": gameUtils.Binding(pygame.K_u),
        "mp": gameUtils.Binding(pygame.K_i),
        "hp": gameUtils.Binding(pygame.K_o),
        "lk": gameUtils.Binding(pygame.K_j),
        "mk": gameUtils.Binding(pygame.K_k),
        "hk": gameUtils.Binding(pygame.K_l),
        "pause": gameUtils.Binding(pygame.K_RETURN)
    })
player2.location = [600, 300]

players = [player1, player2]

# Game loop stuffs
done = False
freeze_players = 0

clock = pygame.time.Clock()

# Menu test stuff
menu_font = pygame.font.SysFont("monospace", 24, False, False)
style = pymenu.Style(menu_font, white, menu_font, green,
    pygame.Rect(0,32,32,32), pygame.Rect(32,32,32,32), pygame.Rect(64,32,32,32),
    pygame.Rect(96,32,32,32), pygame.Rect(32,0,32,32), pygame.Rect(0,0,32,32),
    pygame.Rect(64,0,32,32), pygame.Rect(96,0,32,32), pygame.Rect(128,32,32,32),
    menu_font, white)
items = list()
items.append("Test 1")
items.append("Test 2")
items.append("Test 3")
items.append("Test 4")
items.append("Test 5")
#menu = pymenu.Menu("../content/menu.jpg", style, items, "Test Header")
#menu_surface = menu.render_menu()

# joystick test stuff
pygame.joystick.init()
print ("%d joysticks found" % pygame.joystick.get_count())

""" Game Loop """
while not(done):

    # update the game clock
    temp_time              = current_time
    current_time           = pygame.time.get_ticks()
    time_since_last_update = current_time - temp_time

    # process events
    input_events = list()
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
        elif event.type == gameUtils.CHANGEFACEEVENT:
            this_player = gameUtils.get_player(event.player, players)
            this_player.facing_left = not this_player.facing_left
            if this_player.facing_left:
                this_player.location = [this_player.location[0] + this_player.cropSize[0],
                                        this_player.location[1]]
            else:
                this_player.location = [this_player.location[0] - this_player.cropSize[0],
                                        this_player.location[1]]
        elif event.type == gameUtils.COLLISIONEVENT:
            print "COLLISION"
            event.hitbox.expired = True
            event.hittee.take_hit(event.damage, event.hitstun, event.stun, event.push)
            freeze_event = pygame.event.Event(gameUtils.FREEZEEVENT,
                                              frames=4)
            pygame.event.post(freeze_event)
        elif event.type == gameUtils.FREEZEEVENT:
            print "FREEZE %d" % event.frames
            freeze_players = event.frames


    # Clear the screen
    screen.fill(white)
            
    # Draw the stage
    color = red
    pygame.draw.rect(screen, color, ground, 5)
       

    """Player Loop"""
    for this_player in players:
        player_number = this_player.player_number
        opponent = gameUtils.get_opponent(player_number, players)
        #player_rect = pygame.Rect(0, 0, this_player.cropSize[0], this_player.cropSize[1])
        #opp_rect = pygame.Rect(0, 0, opponent.cropSize[0], opponent.cropSize[1])
        player_rect = this_player.bounding_box
        opp_rect = opponent.bounding_box
        player_rect = gameUtils.trans_rect_to_world(player_rect, this_player.location, this_player.facing_left)
        opp_rect = gameUtils.trans_rect_to_world(opp_rect, opponent.location, opponent.facing_left)

        # push boxes
        player_push = this_player.get_current_move().animation.get_current_frame().push_box
        player_push.rect = gameUtils.trans_rect_to_world(player_push.rect, this_player.location, this_player.facing_left)
        opp_push = opponent.get_current_move().animation.get_current_frame().push_box
        opp_push.rect = gameUtils.trans_rect_to_world(opp_push.rect, opponent.location, opponent.facing_left)

        # update input states
        this_player.last_inputs = copy.deepcopy(this_player.current_inputs)
        this_player.current_inputs = this_player.inputState.getInputState(events)
        this_player.inputState.buffer.update_times(time_since_last_update)
        this_player.inputState.buffer.expireInputs()

        if freeze_players == 0: 
            if player_rect.colliderect(ground):
                collisionShift = gameUtils.getMinTransVect(player_rect, ground)
                this_player.playerForces.append([0, collisionShift[1]])
                this_player.onGround = True
                this_player.playerVel[1] = 0

            # is the player pushing into the opponent
            if player_push.rect.colliderect(opp_push.rect):
                mtv = gameUtils.get_horizontal_translation(player_push.rect, opp_push.rect)
                opponent.location[0] += -1 * mtv

            # Check facing
            if (this_player.onGround and 
                not(any(s in this_player.states for s in [player.PlayerState.ATTACKING,
                                                      player.PlayerState.HIT,
                                                      player.PlayerState.HITSTUN,
                                                      player.PlayerState.LAYING]))):
                # in a possible state where player can change face
               #      check orientation compared to other player
                if (this_player.location[0] < opponent.location[0]):
                    if this_player.facing_left:
                       face_event = pygame.event.Event(gameUtils.CHANGEFACEEVENT,
                                                       player=player_number) 
                       pygame.event.post(face_event) 
                else:
                    if not this_player.facing_left:
                       face_event = pygame.event.Event(gameUtils.CHANGEFACEEVENT,
                                                       player=player_number) 
                       pygame.event.post(face_event)   

            # Check for collisions
            current_frame = this_player.get_current_move().animation.get_current_frame()
            opponent_frame = opponent.get_current_move().animation.get_current_frame()
            for hitbox in current_frame.hitboxes:
                if hitbox.hitActive and not(hitbox.expired):
                    for opp_hitbox in opponent_frame.hitboxes:
                        if opp_hitbox.hurtActive:
                            trans_box =  gameUtils.trans_rect_to_world(hitbox.rect, 
                                                                       this_player.location, 
                                                                       this_player.facing_left) 
                            opp_trans_box = gameUtils.trans_rect_to_world(opp_hitbox.rect,
                                                                          opponent.location,
                                                                          opponent.facing_left)
                            if trans_box.colliderect(opp_trans_box):
                                collide_event = pygame.event.Event(gameUtils.COLLISIONEVENT,
                                                                   hitter=this_player, hittee=opponent,
                                                                   hitbox=hitbox, hurtbox=opp_hitbox,
                                                                   damage=hitbox.damage, stun=hitbox.stun,
                                                                   hitstun=hitbox.hitstun, push=hitbox.push
                                                                   )
                                pygame.event.post(collide_event)

            this_player.update()
        else:
            freeze_players -= 1

        # Draw player image
        new_img = this_player.playerImage if not this_player.facing_left else \
            pygame.transform.flip(this_player.playerImage, True, False)
        current_frame = this_player.moves[this_player.current_move].animation.get_current_frame()
        cropRect = pygame.Rect(current_frame.image_loc[0], current_frame.image_loc[1], 
                               current_frame.crop_size[0], current_frame.crop_size[1])
        draw_location = this_player.location if not this_player.facing_left else \
            (this_player.location[0] - cropRect[2], this_player.location[1])
        if this_player.facing_left:
            cropRect = gameUtils.get_reverse_crop(new_img, cropRect)
        screen.blit(new_img, draw_location, cropRect)    
        if draw_hitboxes:
            for hitbox in current_frame.hitboxes:
                if hitbox.hitActive:
                    if hitbox.hurtActive:
                        color = purple
                    else:
                        color = red
                elif hitbox.hurtActive:
                    color = blue
                else:
                    color = green
                offsetBox = pygame.Rect(hitbox.rect[0], hitbox.rect[1],
                                        hitbox.rect[2], hitbox.rect[3])
                offsetBox = gameUtils.trans_rect_to_world(offsetBox,
                                                          this_player.location,
                                                          this_player.facing_left)
                pygame.draw.rect(screen, color, offsetBox, 2)

        pygame.draw.rect(screen, black, player_rect, 2)
        pygame.draw.rect(screen, purple, player_push, 2)

        # Draw projectiles
        for projectile in this_player.active_projectiles:
            current_frame = projectile.animation.get_next_frame()
            cropRect = pygame.Rect(current_frame.image_loc[0],
                                   current_frame.image_loc[1],
                                   current_frame.crop_size[0],
                                   current_frame.crop_size[1])
            draw_location = projectile.location if not projectile.moving_left else \
                (projectile.location[0] - cropRect[2], projectile.location[1])
            screen.blit(this_player.playerImage, draw_location, cropRect)
            if draw_hitboxes:
                color = white
                for hitbox in current_frame.hitboxes:
                    if hitbox.hitActive:
                        if hitbox.hurtActive:
                            color = purple
                        else:
                            color = red
                    elif hitbox.hurtActive:
                        color = blue
                    else:
                        color = green
                    offsetBox = pygame.Rect(hitbox.rect[0], hitbox.rect[1],
                                            hitbox.rect[2], hitbox.rect[3])
                    offsetBox = gameUtils.trans_rect_to_world(offsetBox,
                                                              projectile.location,
                                                              projectile.moving_left)
                    pygame.draw.rect(screen, color, offsetBox, 2)



    # Draw debug info
    if debug:
        states          = debugFont.render("States: %s" % ", ".join(str(n) for n in player1.states), 1, black)
        onGround        = debugFont.render("On Ground: " + str(player1.onGround), 1, black)
        current_move    = debugFont.render("Current Move: " + str(player1.current_move), 1, black)
        location        = debugFont.render("Location: " + str(player1.location), 1, black)
        velocity        = debugFont.render("Velocity: " + str(player1.playerVel), 1, black)
        projectiles     = debugFont.render("Num Projectiles: " + str(len(player1.active_projectiles)), 1, black)
        attacking       = debugFont.render("Attacking: " + str(player1.attacking), 1, black)

        up              = debugFont.render(str(int(player1.current_inputs["up"])), 1, black)
        down            = debugFont.render(str(int(player1.current_inputs["down"])), 1, black)
        left            = debugFont.render(str(int(player1.current_inputs["left"])), 1, black)
        right           = debugFont.render(str(int(player1.current_inputs["right"])), 1, black)
        lp              = debugFont.render(str(int(player1.current_inputs["lp"])), 1, black)
        mp              = debugFont.render(str(int(player1.current_inputs["mp"])), 1, black)
        hp              = debugFont.render(str(int(player1.current_inputs["hp"])), 1, black)
        lk              = debugFont.render(str(int(player1.current_inputs["lk"])), 1, black)
        mk              = debugFont.render(str(int(player1.current_inputs["mk"])), 1, black)
        hk              = debugFont.render(str(int(player1.current_inputs["hk"])), 1, black)

        debug_y = 0

        screen.blit(states, (0, debug_y))
        debug_y += 18
        screen.blit(onGround, (0, debug_y))
        debug_y += 18
        screen.blit(current_move, (0, debug_y))
        debug_y += 18
        screen.blit(location, (0, debug_y))
        debug_y += 18
        screen.blit(velocity, (0, debug_y))
        debug_y += 18
        screen.blit(projectiles, (0, debug_y))
        debug_y += 18
        screen.blit(attacking, (0, debug_y))

        debug_y += 9
        screen.blit(up, (25, debug_y))
        debug_y += 10  
        screen.blit(left, (0, debug_y))
        screen.blit(right, (50, debug_y))
        debug_y += 35
        screen.blit(down, (25, debug_y))
        debug_y -= 25
        screen.blit(lp, (65, debug_y))
        screen.blit(mp, (80, debug_y))
        screen.blit(hp, (95, debug_y))
        debug_y += 15
        screen.blit(lk, (65, debug_y))
        screen.blit(mk, (80, debug_y))
        screen.blit(hk, (95, debug_y))

        input_buffer_x = 300
        input_buffer_y = 0
        for buffered_input in player1.inputState.buffer.buffer:
            current_output = debugFont.render(buffered_input.inputName, 1, black)
            screen.blit(current_output, (input_buffer_x, input_buffer_y))
            input_buffer_y += 18


    # draw menu test stuff
    #menu_surface = menu.render_menu()
    #screen.blit(menu_surface, (250, 0))

    pygame.display.flip()
            
    # Limit to 20 FPS
    clock.tick(20)
    
# End the game
pygame.quit()
