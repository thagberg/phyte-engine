from collections import defaultdict

import pygame
from ocempgui.widgets import *
from ocempgui.widgets.components import *
from ocempgui.widgets.Constants import *

import hitbox_draw
from frame_definition import FrameDefinitionFrame
from hitbox_draw import HitBoxDefinitionFrame
from animation_definition import AnimationDefinitionFrame
from input_definition import InputDefinitionFrame
from move_definition import MoveDefinitionFrame
from rule_definition import RuleDefinitionFrame
from common import *


SCREEN_SIZE = (1300, 700)
EDITOR_SIZE = (SCREEN_SIZE[0] - 300, SCREEN_SIZE[1] * 0.9)
EDITOR_OFFSET = (200, int(SCREEN_SIZE[1]*0.1/2))

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
#context = defaultdict(ListItemCollection)
context = defaultdict(object)
context['animations'] = ListItemCollection()
context['inputs'] = ListItemCollection()
context['moves'] = ListItemCollection()
context['rules'] = ListItemCollection()
context['components'] = ListItemCollection()

def draw_editor(surface):
    screen.blit(surface, EDITOR_OFFSET)

def activate_tab():
    global current_tab
    re.color = GRAY
    editor_surface.fill(TRANS)
    tab = tab_list.get_selected()[0]
    if current_tab is not None:
        current_tab.deactivate()
    tab.activate()
    current_tab = tab

# GUI elements
tab_list = ScrolledList(175, int(SCREEN_SIZE[1]*0.9))
re.add_widget(tab_list)
tab_list.topleft = (10, int(SCREEN_SIZE[1]*0.1/2))
input_tab = InputDefinitionFrame(re, editor_surface, context, EDITOR_OFFSET)
tab_list.items.append(input_tab)
animation_tab = AnimationDefinitionFrame(re, editor_surface, context, EDITOR_OFFSET)
tab_list.items.append(animation_tab)
frame_tab = FrameDefinitionFrame(re, editor_surface, context, EDITOR_OFFSET)
tab_list.items.append(frame_tab)
box_tab = HitBoxDefinitionFrame(re, editor_surface, context, image, EDITOR_OFFSET)
tab_list.items.append(box_tab)
move_tab = MoveDefinitionFrame(re, editor_surface, context, EDITOR_OFFSET)
tab_list.items.append(move_tab)
rule_tab = RuleDefinitionFrame(re, editor_surface, context, EDITOR_OFFSET)
tab_list.items.append(rule_tab)
tab_list.connect_signal(SIG_SELECTCHANGED, activate_tab)


running = True
while(running):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # update the current tab and draw it to editor surface
    if current_tab is not None:
        current_tab.update(events)

    # pass events to ocempgui renderer
    re.distribute_events(*events)

    # draw the editor pane
    draw_editor(editor_surface)

    pygame.display.flip()
