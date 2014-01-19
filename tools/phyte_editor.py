import pygame
from ocempgui.widgets import *
from ocempgui.widgets.components import *
from ocempgui.widgets.Constants import *

import hitbox_draw
from frame_definition import FrameDefinitionFrame
from common import *


SCREEN_SIZE = (1000, 700)
EDITOR_SIZE = (SCREEN_SIZE[0] - 330, SCREEN_SIZE[1] * 0.9)
EDITOR_OFFSET = (320, int(SCREEN_SIZE[1]*0.1/2))

MOUSE_LEFT = 1
MOUSE_RIGHT = 3

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
editor_surface = pygame.Surface(EDITOR_SIZE)
editor_surface = editor_surface.convert_alpha()
editor_surface.fill(TRANS)
image = pygame.image.load('../content/sticksheet.png')

# set up GUI renderer
re = Renderer()
re.screen = screen
re.title = 'Hitbox Definition'
re.color = GRAY

# shtuff
current_tab = None

def draw_editor(surface):
    screen.blit(surface, EDITOR_OFFSET)

def activate_tab(tab):
    global current_tab
    if current_tab is not None:
        current_tab.deactivate()
    current_tab = tab
    tab.activate()

# GUI elements
tab_list = ScrolledList(300, int(SCREEN_SIZE[1]*0.9))
re.add_widget(tab_list)
tab_list.topleft = (10, int(SCREEN_SIZE[1]*0.1/2))
frame_tab = FrameDefinitionFrame(re, editor_surface, image, EDITOR_OFFSET)
tab_list.items.append(frame_tab)
tab_list.connect_signal(SIG_SELECTCHANGED, activate_tab, frame_tab)


running = True
while(running):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # update the current tab and draw it to editor surface
    if current_tab is not None:
        current_tab.update(events)

    # draw the editor pane
    draw_editor(editor_surface)

    # pass events to ocempgui renderer
    re.distribute_events(*events)

    pygame.display.flip()
