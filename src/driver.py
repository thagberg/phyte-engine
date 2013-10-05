#!/usr/bin/python

import pygame
import gameUtils
import playerUtils
import animation
import move
import physics2d
import engine
import inputs
import factory
import entity
import graphics2d
import text
import common
from events import *

# Define colors
black  = (   0,   0,   0)
white  = ( 255, 255, 255)
red    = ( 255,   0,   0)
green  = (   0, 255,   0)
blue   = (   0,   0, 255)
yellow = ( 255, 255,   0)
purple = ( 255,   0, 255)
trans  = (   0, 253, 255)

# important stuffs
screen_size = (1200, 900)
current_time = pygame.time.get_ticks()
time_since_last_update = 0
system_events = [pygame.QUIT]

# initialize pygame
pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode(screen_size)
screen.set_alpha(None)
screen.set_colorkey((0,255,255))
pygame.display.set_caption("Fighting Game Engine Test")
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

done = False

# initialize systems
eng = engine.PygameEngine()
# initialize object factory
factory = factory.ComponentFactory(eng.process_event)
#ani = animation.AnimationSystem()
#mov = move.MoveSystem()
#phy = physics2d.PhysicsSystem()
#eng.install_system(ani, (ANIMATIONCOMPLETE,ANIMATIONACTIVATE,
#                        ANIMATIONDEACTIVATE))
#eng.install_system(mov, (MOVECHANGE,MOVERESET,MOVEACTIVATE,
#                        MOVEDEACTIVATE))
#eng.install_system(phy, (ADDFORCE,ADDPHYSICSCOMPONENT,
#                        REMOVEPHYSICSCOMPONENT))

## TESTING ##
# input test object
inp = inputs.InputSystem(factory)
eng.install_system(inp, (ADDINPUTCOMPONENT, REMOVEINPUTCOMPONENT,
                         UPDATEBINDINGS, KEYDOWN, KEYUP, JOYBUTTONDOWN, 
                         JOYBUTTONUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, 
                         JOYAXISMOTION))
t_entity = factory.create_entity()
t_bindings = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}
t_inp_component = factory.create_component('input', device=-1,
                                           entity_id=t_entity.entity_id,
                                           bindings=t_bindings)
gra = graphics2d.GraphicsSystem(screen, factory)
eng.install_system(gra, (ADDGRAPHICSCOMPONENT, REMOVEGRAPHICSCOMPONENT,
                         CHANGECROP, CHANGEDEST, CHANGESURFACE,
                         CHANGEDISPLAY, CHANGEZLEVEL))

# text test object
tex = text.TextSystem(factory)
eng.install_system(tex, (ADDTEXTCOMPONENT, REMOVETEXTCOMPONENT,
                          UPDATETEXT))
t_tex_comp = factory.create_component('text', entity_id=t_entity.entity_id,
                                      text='Test Text', loc=[0,0], style=dict())

# graphic test objects
g_entity = factory.create_entity()
g_surface = pygame.image.load('../content/sticksheet.png')
g_comp = factory.create_component('graphics', entity_id=g_entity.entity_id,
                                  surface=g_surface, dest=[200,200],
                                  area=[200,200,100,100])

# animation test objects
ani = animation.AnimationSystem(factory)
eng.install_system(ani, (ANIMATIONCOMPLETE, ANIMATIONACTIVATE,
                         ANIMATIONDEACTIVATE, ANIMATIONSTEP,
                         ANIMATIONJUMP))
a_entity = factory.create_entity()
f_one = factory.create_component('fra', entity_id=a_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[0,0,64,128],
                                 repeat=20, push_box=None)
f_two = factory.create_component('fra', entity_id=a_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[66,0,64,128],
                                 repeat=3, push_box=None)
f_tre = factory.create_component('fra', entity_id=a_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[131,0,64,128],
                                 repeat=3, push_box=None)
frames = [f_one, f_two, f_tre]
ani_one = factory.create_component('ani', entity_id=a_entity.entity_id,
                                   frames=frames, loop=True,
                                   graphic=g_comp)


print "Joysticks available: %d" % len(joysticks)
for joy in joysticks:
    joy.init()
    print "Info for joy id: %d" % joy.get_id()
    print "\tName: %s" % joy.get_name()
    print "\tNum Axes: %d" % joy.get_numaxes()
    print "\tNum Balls: %d" % joy.get_numballs()
    print "\tNum Buttons: %d" % joy.get_numbuttons()

# Game loop
while not(done):
    last_time = current_time
    current_time = pygame.time.get_ticks()
    time_since_last_update = current_time - last_time
    screen.fill(common.WHITE)
    events = pygame.event.get()

    eng.update(time_since_last_update, events)

    # system processing stuffs
    for event in filter(lambda x: x.type in system_events, events):
        if event.type == pygame.QUIT:
            print 'QUITTING NOW'
            done = True

    pygame.display.flip()
    events = list()
