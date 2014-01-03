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
import debug
import player
import execute
import state
import movement
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
clock = pygame.time.Clock()

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

## TESTING ##

### CREATE SYSTEMS HERE ###
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
                         CHANGEDISPLAY, CHANGEZLEVEL), stage=2)

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
                         REMOVEMOVECOMPONENT))

movm = movement.MovementSystem(factory)
eng.install_system(movm, (ADDMOVEMENTCOMPONENT, REMOVEMOVEMENTCOMPONENT,
                          ACTIVATEMOVEMENTCOMPONENT, DEACTIVATEMOVEMENTCOMPONENT))

exe = execute.ExecutionSystem(factory)
eng.install_system(exe, (ADDEXECUTIONCOMPONENT, REMOVEEXECUTIONCOMPONENT,
                         ACTIVATEEXECUTIONCOMPONENT,
                         DEACTIVATEEXECUTIONCOMPONENT))

sta = state.StateSystem(factory)
eng.install_system(sta, (ADDSTATECOMPONENT, REMOVESTATECOMPONENT))

phy = physics2d.PhysicsSystem(factory)
eng.install_system(phy, (PHYSICSEVENT, ADDFORCE, ADDPHYSICSCOMPONENT,
                         REMOVEPHYSICSCOMPONENT, ADDPHYSICSCOMPONENTACTIVE,
                         REMOVEPHYSICSCOMPONENTACTIVE, ADDCOLLIDEABLE,
                         REMOVECOLLIDEABLE, SETCOLLIDEABLES,
                         CLEARCOLLIDEABLES))

deb = debug.DebugSystem(screen, factory)
eng.install_system(deb, (ADDDEBUGCOMPONENT, REMOVEDEBUGCOMPONENT,
                         UPDATEDEBUGCOMPONENT))

pla = player.PlayerSystem(factory)
eng.install_system(pla, (ADDPLAYERCOMPONENT, REMOVEPLAYERCOMPONENT,
                         MOVEDEACTIVATE))

# input test object
player_entity = factory.create_entity()
t_entity = factory.create_entity()
player_bindings = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}
player_inp_component = factory.create_component('input', device=-1,
                                           entity_id=player_entity.entity_id,
                                           bindings=player_bindings)


# text test object
t_tex_comp = factory.create_component('text', entity_id=t_entity.entity_id,
                                      text='Test Text', loc=[0,0], style=dict())

# graphic test objects
player_surface = pygame.image.load('../content/sticksheet.png')
g_comp = factory.create_component('graphics', entity_id=player_entity.entity_id,
                                  surface=player_surface, dest=[200,200],
                                  area=[200,200,100,100])

# animation test objects
f_one = factory.create_component('fra', entity_id=player_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[0,128,64,128],
                                 repeat=20, push_box=None)
f_two = factory.create_component('fra', entity_id=player_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[66,128,64,128],
                                 repeat=20, push_box=None)
f_tre = factory.create_component('fra', entity_id=player_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[131,128,64,128],
                                 repeat=20, push_box=None)
frames = [f_one, f_two, f_tre]
ani_one = factory.create_component('ani', entity_id=player_entity.entity_id,
                                   frames=frames, loop=True,
                                   graphic=g_comp)
# animation 2
f2_one = factory.create_component('fra', entity_id=player_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[0,0,64,128],
                                 repeat=20, push_box=None)
f2_two = factory.create_component('fra', entity_id=player_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[66,0,64,128],
                                 repeat=20, push_box=None)
f2_tre = factory.create_component('fra', entity_id=player_entity.entity_id,
                                 hitboxes=None, force=[0,0], crop=[131,0,64,128],
                                 repeat=20, push_box=None)
f2_four = factory.create_component('fra', entity_id=player_entity.entity_id,
                                   hitboxes=None, force=[0,0], crop=[196,0,64,128],
                                   repeat=20, push_box=None)
f2_five = factory.create_component('fra', entity_id=player_entity.entity_id,
                                   hitboxes=None, force=[0,0], crop=[261,0,64,128],
                                   repeat=20, push_box=None)
frames2 = [f2_one, f2_two, f2_tre, f2_four, f2_five]
ani_two = factory.create_component('ani', entity_id=player_entity.entity_id,
                                   frames=frames2, loop=True,
                                   graphic=g_comp)
# jump animation
jf_one = factory.create_component('fra', entity_id=player_entity.entity_id,
                                  hitboxes=None, force=[0,0], crop=[0,259,64,128],
                                  repeat=0, push_box=None)
jump_ani = factory.create_component('ani', entity_id=player_entity.entity_id,
                                    frames=[jf_one], loop=True, graphic=g_comp)

# move test objects
m_inputs = ['right']
move_one = factory.create_component('move', entity_id=player_entity.entity_id,
                                    name='testmove',
                                    animation=ani_one,
                                    inputs=m_inputs)
m2_inputs = []
move_two = factory.create_component('move', entity_id=player_entity.entity_id,
                                     name='neutral',
                                     animation=ani_two,
                                     inputs=m2_inputs)
jump_move_inputs = ['up']
jump_move = factory.create_component('move', entity_id=player_entity.entity_id,
                                     name='jump', animation=jump_ani,
                                     inputs=jump_move_inputs)

# movement test objects
g_movement_comp = factory.create_component('movement', 
                                           entity_id=player_entity.entity_id,
                                           body=g_comp.dest, 
                                           velocity=[0,0])
movm_comp = factory.create_component('movement', 
                                     entity_id=player_entity.entity_id,
                                     body=g_movement_comp.velocity, 
                                     velocity=[5, 0])
jump_movement_comp = factory.create_component('movement', 
                                              entity_id=player_entity.entity_id,
                                              body=g_movement_comp.velocity, 
                                              velocity=[0,0],
                                              inc_velocity=[0,-20])
gravity_movement_comp = factory.create_component('movement', 
                                                 entity_id=player_entity.entity_id,
                                                 body=g_movement_comp.velocity, 
                                                 velocity=[0,3])
def friction_movement_vel():
    friction = [0,0]
    x = g_movement_comp.velocity[0]
    abs_x = abs(x)
    if abs_x > 0:
        if abs_x >= 2:
            friction[0] = 2
        else:
            friction[0] = abs_x
        if x > 0:
            friction[0] = 0 - friction[0]
    return friction
friction_movement_comp = factory.create_component('varmovement',
                                                  entity_id=player_entity.entity_id,
                                                  body=g_movement_comp.velocity,
                                                  velocity_func=friction_movement_vel)

# execution test objects

exe_one = factory.create_component('exe', entity_id=player_entity.entity_id,
                                    executables=[jump_move, move_one, move_two], 
                                    inputs=player_inp_component)

# state test objects

rule_one = factory.create_component('rule', name='test', operator='eq',
                                    value=True)
state_one = factory.create_component('state', entity_id=player_entity.entity_id,
                                     rules=[rule_one],
                                     activation_event_type=ACTIVATEEXECUTIONCOMPONENT,
                                     deactivation_event_type=DEACTIVATEEXECUTIONCOMPONENT,
                                     activation_component=exe_one,
                                     rule_values={'test':True})
movement_rule = factory.create_component('rule', name='move', operator='eq',
                                         value=True)
movement_state = factory.create_component('state', entity_id=player_entity.entity_id,
                                          rules=[movement_rule],
                                          activation_event_type=ACTIVATEMOVEMENTCOMPONENT,
                                          deactivation_event_type=DEACTIVATEMOVEMENTCOMPONENT,
                                          activation_component=movm_comp,
                                          rule_values={'move':lambda: move_one.active})
jump_rule = factory.create_component('rule', name='jump', operator='eq',
                                     value=True)
#jump_rule_value = lambda: jump_move.active and jump_movement_comp.velocity[1] > 0
jump_rule_value = lambda: jump_move.active
jump_state = factory.create_component('state', entity_id=player_entity.entity_id,
                                      rules=[jump_rule],
                                      activation_event_type=ACTIVATEMOVEMENTCOMPONENT,
                                      deactivation_event_type=DEACTIVATEMOVEMENTCOMPONENT,
                                      activation_component=jump_movement_comp,
                                      rule_values={'jump': jump_rule_value})
moveable_rule = factory.create_component('rule', name='moveable', operator='eq',
                                         value=True)
moveable_rule_value = lambda: True
moveable_state = factory.create_component('state', entity_id=player_entity.entity_id,
                                          rules=[moveable_rule],
                                          activation_event_type=ACTIVATEMOVEMENTCOMPONENT,
                                          deactivation_event_type=DEACTIVATEMOVEMENTCOMPONENT,
                                          activation_component=g_movement_comp,
                                          rule_values={'moveable': moveable_rule_value})
gravity_rule = factory.create_component('rule', name='gravity', operator='ne', value=0)
gravity_rule_value = lambda: g_movement_comp.velocity[1]
gravity_state = factory.create_component('state', entity_id=player_entity.entity_id,
                                         rules=[gravity_rule],
                                         activation_event_type=ACTIVATEMOVEMENTCOMPONENT,
                                         deactivation_event_type=DEACTIVATEMOVEMENTCOMPONENT,
                                         activation_component=gravity_movement_comp,
                                         rule_values={'gravity': gravity_rule_value})
friction_rule = factory.create_component('rule', name='friction', operator='gt', value=0)
friction_rule_value = lambda: abs(g_movement_comp.velocity[0])
friction_state = factory.create_component('state', entity_id=player_entity.entity_id,
                                          rules=[friction_rule],
                                          activation_event_type=ACTIVATEMOVEMENTCOMPONENT,
                                          deactivation_event_type=DEACTIVATEMOVEMENTCOMPONENT,
                                          activation_component=friction_movement_comp,
                                          rule_values={'friction': friction_rule_value})

# physics test objects

p1_entity = factory.create_entity()
p2_entity = factory.create_entity()

# debug test objects

d_entity = factory.create_entity()
d_rect = pygame.Rect(200, 350, 100, 100)
d_comp = factory.create_component('deb', entity_id=d_entity.entity_id,
                                  rect=d_rect)
d_text_comp = factory.create_component('text', entity_id=player_entity.entity_id,
                                       text=str(g_comp.area), loc=[0, 100], style=dict())
d2_comp = factory.create_component('deb', entity_id=player_entity.entity_id, text=d_text_comp,
                                   get_value=lambda: g_comp.area)
d3_text_comp = factory.create_component('text', entity_id=player_entity.entity_id,
                                         text='%s:%s' % (move_one.name, str(move_one.active)), 
                                         loc=[0, 120], style=dict())
d3_comp = factory.create_component('deb', entity_id=player_entity.entity_id, text=d3_text_comp,
                                   get_value=lambda: '%s:%s' % (move_one.name, str(move_one.active)))
d4_text_comp = factory.create_component('text', entity_id=player_entity.entity_id,
                                         text='%s:%s' % (move_two.name, str(move_two.active)), 
                                         loc=[0, 140], style=dict())
d4_comp = factory.create_component('deb', entity_id=player_entity.entity_id, text=d4_text_comp,
                                   get_value=lambda: '%s:%s' % (move_two.name, str(move_two.active)))
jump_text_comp = factory.create_component('text', entity_id=player_entity.entity_id,
                                          text='%s:%s' % (jump_move.name, jump_move.active),
                                          loc=[0,160], style=dict())
jump_deb_comp = factory.create_component('deb', entity_id=player_entity.entity_id, text=jump_text_comp,
                                         get_value=lambda: '%s:%s' %(jump_move.name, jump_move.active))
ani1_text_comp = factory.create_component('text', entity_id=player_entity.entity_id,
                                          text='%s-%s-%s' % (ani_one.active, ani_one.current_index, len(ani_one.frames)), 
                                          loc=[0,180], style=dict())
ani1_debug_comp = factory.create_component('deb', entity_id=player_entity.entity_id, text=ani1_text_comp,
                                           get_value=lambda: '%s-%s-%s' % (ani_one.active, ani_one.current_index, len(ani_one.frames)))
ani2_text_comp = factory.create_component('text', entity_id=player_entity.entity_id,
                                          text='%s-%s-%s' % (ani_two.active, ani_two.current_index, len(ani_two.frames)),
                                          loc=[0,200], style=dict())
ani2_debug_comp = factory.create_component('deb', entity_id=player_entity.entity_id, text=ani2_text_comp,
                                           get_value=lambda: '%s-%s-%s' % (ani_two.active, ani_two.current_index, len(ani_two.frames)))
jani_text_comp = factory.create_component('text', entity_id=player_entity.entity_id,
                                          text='%s-%s-%s' % (jump_ani.active, jump_ani.current_index, len(jump_ani.frames)),
                                          loc=[0,220], style=dict())
jani_debug_comp = factory.create_component('deb', entity_id=player_entity.entity_id, text=jani_text_comp,
                                           get_value=lambda: '%s-%s-%s' % (jump_ani.active, jump_ani.current_index, len(jump_ani.frames)))

# FPS output stuff
fps = 0
fps_entity = factory.create_entity()
fps_text_component = factory.create_component('text', entity_id=fps_entity.entity_id,
                                              text=str(fps), loc=[10, 400], style=dict())
fps_debug_component = factory.create_component('deb', entity_id=fps_entity.entity_id,
                                               text=fps_text_component,
                                               get_value=lambda: '%d' % fps)

# player test objects

p_entity = factory.create_entity()
p_loc = factory.create_component('loc', entity_id=p_entity.entity_id,
                                 point=[400,500])
p_bindings = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT
}
p_inpbuf = factory.create_component('inbuf', entity_id=p_entity.entity_id,
                                    expire_time=2000)
p_input = factory.create_component('input', entity_id=p_entity.entity_id,
                                   device=-1, bindings=p_bindings,
                                   inp_buffer=p_inpbuf)
p_comp = factory.create_component('pla', entity_id=p_entity.entity_id,
                                  location=p_loc, inputs=p_input,
                                  input_device=-1, graphic=g_comp)


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
    fps = 1000 / time_since_last_update
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
    clock.tick(60) 
