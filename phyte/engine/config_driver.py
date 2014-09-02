#!/usr/bin/python
from collections import defaultdict

import pygame

from engine import load_config
from engine import game_engine
from engine import animation
from engine import move
from engine import physics2d
from engine import inputs
from engine import factory
from engine import entity
from engine import graphics2d
from engine import text
from engine import common
from engine import debug
from engine import player
from engine import execute
from engine import state
from engine import movement
from engine.events import *

import globals

SCREEN_SIZE = (800, 600)
current_time = pygame.time.get_ticks()
time_since_last_update = 0
system_events = [pygame.QUIT]
clock = pygame.time.Clock()

pygame.init()
pygame.joystick.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.set_alpha(None)
pygame.display.set_caption('Engine Test With Loaded Configuration')
config_file_name = '../../content/debug_test12'

done = False

eng = game_engine.PygameEngine()
factory = factory.ComponentFactory(eng.process_event)

# engine systems
inp = inputs.InputSystem(factory)
eng.install_system(inp, (ADDINPUTCOMPONENT, REMOVEINPUTCOMPONENT,
                         UPDATEBINDINGS, KEYDOWN, KEYUP, JOYBUTTONDOWN, 
                         JOYBUTTONUP, MOUSEBUTTONDOWN, MOUSEBUTTONUP, 
                         JOYAXISMOTION))

inpb = inputs.InputBufferSystem(factory)
eng.install_system(inpb, (ADDINPUTBUFFERCOMPONENT, REMOVEINPUTBUFFERCOMPONENT,
                          BUFFERINPUT))

gra = graphics2d.GraphicsSystem(screen, factory)
eng.install_system(gra, (ADDGRAPHICSCOMPONENT, REMOVEGRAPHICSCOMPONENT,
                         CHANGECROP, CHANGEDEST, CHANGESURFACE,
                         CHANGEDISPLAY, CHANGEZLEVEL,
                         ACTIVATEGRAPHICSCOMPONENT, DEACTIVATEGRAPHICSCOMPONENT), 
                   stage=2)

tex = text.TextSystem(factory)
eng.install_system(tex, (ADDTEXTCOMPONENT, REMOVETEXTCOMPONENT,
                          UPDATETEXT))

ani = animation.AnimationSystem(factory)
eng.install_system(ani, (ANIMATIONCOMPLETE, ANIMATIONACTIVATE,
                         ANIMATIONDEACTIVATE, ANIMATIONSTEP,
                         ANIMATIONJUMP, ADDANIMATIONCOMPONENT,
                         REMOVEANIMATIONCOMPONENT))

mov = move.MoveSystem(factory)
eng.install_system(mov, (MOVEEVENT, MOVECHANGE, MOVERESET, MOVEACTIVATE,
                         MOVEDEACTIVATE, ADDMOVECOMPONENT,
                         REMOVEMOVECOMPONENT, ANIMATIONCOMPLETE))

sta = state.StateSystem(factory)
eng.install_system(sta, (ADDSTATECOMPONENT, REMOVESTATECOMPONENT,
                         ACTIVATESTATEVALUE, DEACTIVATESTATEVALUE))

movm = movement.MovementSystem(factory)
eng.install_system(movm, (ADDMOVEMENTCOMPONENT, REMOVEMOVEMENTCOMPONENT,
                          ACTIVATEMOVEMENTCOMPONENT, DEACTIVATEMOVEMENTCOMPONENT,
                          APPLYINCIDENTALMOVEMENTCOMPONENT))

phy = physics2d.PhysicsSystem(factory)
eng.install_system(phy, (PHYSICSEVENT, ADDFORCE, ADDPHYSICSCOMPONENT,
                         REMOVEPHYSICSCOMPONENT, ACTIVATEPHYSICSCOMPONENT,
                         DEACTIVATEPHYSICSCOMPONENT, COLLISION))

exe = execute.ExecutionSystem(factory)
eng.install_system(exe, (ADDEXECUTIONCOMPONENT, REMOVEEXECUTIONCOMPONENT,
                         ACTIVATEEXECUTIONCOMPONENT,
                         DEACTIVATEEXECUTIONCOMPONENT))

deb = debug.DebugSystem(screen, factory)
eng.install_system(deb, (ADDDEBUGCOMPONENT, REMOVEDEBUGCOMPONENT,
                         UPDATEDEBUGCOMPONENT, ACTIVATEDEBUGCOMPONENT,
                         DEACTIVATEDEBUGCOMPONENT))

pla = player.PlayerSystem(factory)
eng.install_system(pla, (ADDPLAYERCOMPONENT, REMOVEPLAYERCOMPONENT,
                         MOVEDEACTIVATE))





# load entities and components from configuration
#globals.game_context = defaultdict(list)
load_config.load(config_file_name, factory, globals.game_context)

# FPS output stuff
fps = 0
fps_entity = factory.create_entity()
fps_loc = factory.create_component('vec2', entity_id=fps_entity.entity_id,
                                   vec=[10, 400])
fps_body = factory.create_component('body', entity_id=fps_entity.entity_id,
                                    body=fps_loc)
fps_text_component = factory.create_component('text', entity_id=fps_entity.entity_id,
                                              text=str(fps), loc=fps_body, style=dict())
fps_debug_component = factory.create_component('deb', entity_id=fps_entity.entity_id,
                                               text=fps_text_component,
                                               get_value=lambda: '%d' % fps)

# create debug components for each solid animation hitbox
comps = ani.components
for comp in comps:
    for frame in comp.frames:
        for box in [x for x in frame.hitboxes if x.solid]:
            hd = factory.create_component('deb',
                                          entity_id=comp.entity_id,
                                          rect=box,
                                          style={'color': (0,0,0,255)},
                                          active=True)

from pdb import set_trace
set_trace()

# Game loop
while not(done):
    last_time = current_time
    current_time = pygame.time.get_ticks()
    time_since_last_update = current_time - last_time
    fps = 1000 / time_since_last_update
    screen.fill(common.WHITE)
    events = pygame.event.get()
    '''for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t:
                eng.update(time_since_last_update, events)
                pygame.display.flip()'''

    eng.update(time_since_last_update, events)

    # system processing stuffs
    for event in filter(lambda x: x.type in system_events, events):
        if event.type == pygame.QUIT:
            print 'QUITTING NOW'
            done = True

    pygame.display.flip()
    events = list()
    clock.tick(5) 
