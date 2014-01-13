import pygame

SCREEN_SIZE = (800, 600)
WHITE = (255,255,255,255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
PURPLE = (255, 0, 255, 255)
YELLOW = (255, 255, 0, 255)
BLACK = (0, 0, 0, 255)

MOUSE_LEFT = 1

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.set_alpha(None)
screen.set_colorkey((0,255,255))
pygame.display.set_caption('Hitbox Definition')


class HitBox(object):
    def __init__(self, rect, hitactive=False, hurtactive=False,
                 blockactive=False):
        self.rect = rect
        self.hitactive = hitactive
        self.hurtactive = hurtactive
        self.blockactive = blockactive


def draw_frame(screen, image, crop):
    dest_x = screen.get_width()/2 - crop[2]/2
    dest_y = screen.get_height()/2 - crop[3]/2
    screen.blit(image, (dest_x, dest_y), crop)

def draw_box(screen, box, offset=(0,0)):
    rect = box.rect.copy()
    rect[0] = rect[0] + offset[0]
    rect[1] = rect[1] + offset[1]
    color = BLACK
    if box.hitactive:
        if box.hurtactive:
            color = PURPLE
        else:
            color = BLUE
    elif box.hurtactive:
        color = RED
    elif box.blockactive:
        color = GREEN
    pygame.draw.rect(screen, color, rect, 1)



image = pygame.image.load('../content/sticksheet.png')
crop = [0,0,64,128]
click_down = False
click_down_pos = []
boxes = []
running = True
while(running):
    screen.fill(WHITE)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_LEFT:
                click_down = True
                click_down_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == MOUSE_LEFT:
                click_down = False
                end_pos = event.pos
                box_width = end_pos[0] - click_down_pos[0]
                box_height = end_pos[1] - click_down_pos[1]
                box = pygame.Rect(click_down_pos[0], click_down_pos[1], box_width, box_height)
                hitbox = HitBox(box, hitactive=True)
                boxes.append(hitbox)

    draw_frame(screen, image, crop)
    if click_down:
        current_pos = pygame.mouse.get_pos()
        box_width = current_pos[0] - click_down_pos[0]
        box_height = current_pos[1] - click_down_pos[1]
        box = pygame.Rect(click_down_pos[0], click_down_pos[1], box_width, box_height)
        hitbox = HitBox(box, hitactive=True)
        draw_box(screen, hitbox)

    for box in boxes:
        draw_box(screen, box)

    pygame.display.flip()
