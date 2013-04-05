import pygame
import player
import gameUtils
import playerUtils
import pymenu

pygame.init()

# Define colors
black = (   0,   0,   0)
white = ( 255, 255, 255)
red   = ( 255,   0,   0)
green = (   0, 255,   0)
blue  = (   0,   0, 255)

# game state stuff
debug = True
debugFont = pygame.font.SysFont("monospace", 15, False, False)
current_time = pygame.time.get_ticks()
time_since_last_udate = 0
hitboxes = True

# Screen stuffs
size = [700,500]
screen = pygame.display.set_mode(size)
screen.set_alpha(None)
screen.set_colorkey((    0, 255, 255))
pygame.display.set_caption("Bam it's a game")

# Initialize the stage
ground = pygame.Rect(0, 450, size[0], 50)

# Initialize a player
player1_config = playerUtils.load_character("stick")
player1 = playerUtils.create_player(player1_config, 1)
player1.inputState = gameUtils.Inputs()
player1.facing_left = False

# Game loop stuffs
done = False

clock = pygame.time.Clock()

# Menu test stuff
menu_font = pygame.font.SysFont("monospace", 24, False, False)
style = pymenu.Style(menu_font, white, menu_font, white,
    pygame.Rect(0,32,32,32), pygame.Rect(32,32,32,32), pygame.Rect(64,32,32,32),
    pygame.Rect(96,32,32,32), pygame.Rect(32,0,32,32), pygame.Rect(0,0,32,32),
    pygame.Rect(64,0,32,32), pygame.Rect(96,0,32,32), pygame.Rect(128,32,32,32))
items = list()
items.append("Test 1")
items.append("Test 2")
items.append("Test 3")
menu = pymenu.Menu("../content/menu.jpg", style, items)
menu_surface = menu.render_menu()

# --- Here's da loop --- #
while not(done):

    # update the game clock
    temp_time              = current_time
    current_time           = pygame.time.get_ticks()
    time_since_last_update = current_time - temp_time

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True

       
    # Logic processing

    playerRect = pygame.Rect(player1.location[0], player1.location[1], player1.cropSize[0], player1.cropSize[1])
    if playerRect.colliderect(ground):
        collisionShift = gameUtils.getMinTransVect(playerRect, ground)
        player1.playerForces.append([0, collisionShift[1]])
        player1.onGround = True
        player1.playerVel[1] = 0
        
    player1.current_inputs = player1.inputState.getInputState(events)
    player1.inputState.buffer.update_times(time_since_last_update)
    player1.inputState.buffer.expireInputs()
    player1.update()
           
    # Graphics processing
    screen.fill(white)
            
    # Draw the stage
    color = red
    pygame.draw.rect(screen, color, ground, 5)
        
    # Draw player image
    new_img = player1.playerImage if not player1.facing_left else pygame.transform.flip(player1.playerImage, True, False)
    cropRect = pygame.Rect(player1.imageLoc[0], player1.imageLoc[1], player1.cropSize[0], player1.cropSize[1])
    if player1.facing_left:
        cropRect = gameUtils.get_reverse_crop(new_img, cropRect)
    screen.blit(new_img, player1.location, cropRect)    
    if hitboxes:
        current_frame = player1.moves[player1.current_move].current_frame
        for hitbox in current_frame.hitboxes:
            if hitbox.hitActive:
                color = red
            elif hitbox.hurtActive:
                color = blue
            else:
                color = green
            offsetBox = [hitbox.rect[0] + player1.location[0],
                         hitbox.rect[1] + player1.location[1],
                         hitbox.rect[2], hitbox.rect[3]]
            pygame.draw.rect(screen, color, offsetBox, 2)

    # Draw projectiles
    for projectile in player1.active_projectiles:
        current_frame = projectile.animation.get_next_frame()
        cropRect = pygame.Rect(current_frame.image_loc[0],
                               current_frame.image_loc[1],
                               current_frame.crop_size[0],
                               current_frame.crop_size[1])
        screen.blit(player1.playerImage, (projectile.location[0], projectile.location[1]), cropRect)
        if hitboxes:
            color = red
            for hitbox in current_frame.hitboxes:
                offsetBox = [hitbox.rect[0] + projectile.location[0],
                             hitbox.rect[1] + projectile.location[1],
                             hitbox.rect[2], hitbox.rect[3]]
                pygame.draw.rect(screen, color, offsetBox, 2)
        
    # Draw player boxes
    for box in player1.playerBoxes:
        color = white
        if box.hitActive:
            color = green
        elif box.hurtActive:
            color = red
        else:
            color = blue
        
        offsetBox = [box.rect[0] + player1.location[0], box.rect[1] + player1.location[1], box.rect[2], box.rect[3]]
            
        pygame.draw.rect(screen, color, offsetBox, 2)


    # Draw debug info
    if debug:
        primary_state   = debugFont.render("Primary State: " + str(player1.primary_state), 1, black)
        secondary_state = debugFont.render("Secondary State: " + str(player1.secondary_state), 1, black)
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

        screen.blit(primary_state, (0, debug_y))
        debug_y += 18
        screen.blit(secondary_state, (0, debug_y))
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
    screen.blit(menu_surface, (250, 0))

    pygame.display.flip()
            
    # Limit to 20 FPS
    clock.tick(20)
    
# End the game
pygame.quit()
