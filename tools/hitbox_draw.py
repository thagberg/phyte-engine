import pygame
from ocempgui.widgets import *
from ocempgui.widgets.components import *
from ocempgui.widgets.Constants import *

SCREEN_SIZE = (1000, 700)
FRAME_SIZE = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]*0.8)

WHITE = (255,255,255,255)
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
PURPLE = (255, 0, 255, 255)
YELLOW = (255, 255, 0, 255)
BLACK = (0, 0, 0, 255)
GRAY = (220, 220, 220, 255)

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
frame_surface = pygame.Surface(FRAME_SIZE)

# set up GUI renderer
re = Renderer()
re.screen = screen
re.title = 'Hitbox Definition'
re.color = GRAY


class HitBox(TextListItem):
    def __init__(self, rect, hitactive=False, hurtactive=False,
                 blockactive=False, solid=False):
        super(HitBox, self).__init__()
        self.rect = rect
        self.hitactive = hitactive
        self.hurtactive = hurtactive
        self.blockactive = blockactive
        self.solid = solid
        self.text = '%s:%s:%s:%s / (%d,%d) - (%d, %d)' % (self.hitactive,
                                                          self.hurtactive,
                                                          self.blockactive,
                                                          self.solid,
                                                          self.rect.x,
                                                          self.rect.y,
                                                          self.rect.width,
                                                          self.rect.height)


    def __str__(self):
        return 

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

def add_box():
    rect = pygame.Rect(int(box_x.text),
                       int(box_y.text),
                       int(box_width.text),
                       int(box_height.text))
    hitactive = hitactive_check.active
    hurtactive = hurtactive_check.active
    blockactive = blockactive_check.active
    solid = solid_check.active
    hitbox = HitBox(rect, hitactive, hurtactive, blockactive, solid)
    box_list.items.append(hitbox)

def cleanup_box(rect):
    # flip the origin corner to the top left if necessary
    if rect.width < 0:
        rect.x = rect.x + rect.width
        rect.width = 0 - rect.width
    if rect.height < 0:
        rect.y = rect.y + rect.height
        rect.height = 0 - rect.height
    box_x.text = str(rect.x)
    box_y.text = str(rect.y)
    box_width.text = str(rect.width)
    box_height.text = str(rect.height)

def set_current_box(selection):
    pass

image = pygame.image.load('../content/sticksheet.png')
crop = [0,0,64,128]
click_down = False
click_down_pos = []
boxes = ListItemCollection()
current_box = None
frame_pos = (SCREEN_SIZE[0]-FRAME_SIZE[0]-10,
             SCREEN_SIZE[1]-FRAME_SIZE[1]-10)
frame_rect = frame_surface.get_rect(center=(frame_pos[0]+frame_surface.get_width()/2,
                                            frame_pos[1]+frame_surface.get_height()/2))

# set up GUI stuff
# define GUI elements
hitactive_check = CheckButton("Hit Active")
hurtactive_check = CheckButton("Hurt Active")
blockactive_check = CheckButton("Block Active")
solid_check = CheckButton("Solid")
box_x_label = Label('Box X')
box_x = Entry()
box_y_label = Label('Box Y')
box_y = Entry()
box_width_label = Label('Box Width')
box_width = Entry()
box_height_label = Label('Box Height')
box_height = Entry()
add_button = Button('Add Box')
box_list = ScrolledList(300, 300, boxes)

re.add_widget(hitactive_check)
re.add_widget(hurtactive_check)
re.add_widget(blockactive_check)
re.add_widget(solid_check)
re.add_widget(box_x_label)
re.add_widget(box_x)
re.add_widget(box_y_label)
re.add_widget(box_y)
re.add_widget(box_width_label)
re.add_widget(box_width)
re.add_widget(box_height_label)
re.add_widget(box_height)
re.add_widget(add_button)
re.add_widget(box_list)

box_x_label.align = ALIGN_LEFT
box_y_label.align = ALIGN_LEFT
box_width_label.align = ALIGN_LEFT
box_height_label.align = ALIGN_LEFT

hitactive_check.topleft = (10, 25)
hurtactive_check.topleft = (10, 50)
blockactive_check.topleft = (10, 75)
solid_check.topleft = (10, 100)
box_x_label.topleft = (150, 25)
box_x.topleft = (225, 25)
box_y_label.topleft = (150, 50)
box_y.topleft = (225, 50)
box_width_label.topleft = (150, 75)
box_width.topleft = (225, 75)
box_height_label.topleft = (150, 100)
box_height.topleft = (225, 100)
add_button.topleft = (320, 145)
box_list.topleft = (10, 140)
box_list.selectionmode = SELECTION_SINGLE

# wire up GUI events
add_button.connect_signal(SIG_CLICKED, add_box)

running = True
while(running):
    #screen.fill(re.color)
    frame_surface.fill(WHITE)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == MOUSE_RIGHT:
                if frame_rect.collidepoint(event.pos):
                    click_down = True
                    translated_pos = (event.pos[0] - frame_pos[0],
                                      event.pos[1] - frame_pos[1])
                    current_box = pygame.Rect(translated_pos, (0,0))
                    box_x.text = str(current_box.x)
                    box_y.text = str(current_box.y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == MOUSE_RIGHT:
                if frame_rect.collidepoint(event.pos):
                    click_down = False
                    end_pos = event.pos
                    translated_pos = (event.pos[0] - frame_pos[0],
                                      event.pos[1] - frame_pos[1])
                    current_box.width = translated_pos[0] - current_box.x
                    current_box.height = translated_pos[1] - current_box.y
                    cleanup_box(current_box)

    # pass events to ocempgui renderer
    re.distribute_events(*events)

    # draw the animation frame
    draw_frame(frame_surface, image, crop)

    # draw temporary click-and-drag box
    if click_down:
        current_pos = pygame.mouse.get_pos()
        translated_pos = (current_pos[0] - frame_pos[0],
                          current_pos[1] - frame_pos[1])
        temp_box = pygame.Rect(current_box.x,
                               current_box.y,
                               translated_pos[0] - current_box.x, 
                               translated_pos[1] - current_box.y) 
        hb = HitBox(temp_box, hitactive=True)
        draw_box(frame_surface, hb)

    # draw the current box
    if current_box:
        hb = HitBox(current_box, hitactive=True)
        draw_box(frame_surface, hb)

    # draw the frame plane to the screen
    screen.blit(frame_surface, frame_pos)

    pygame.display.flip()
