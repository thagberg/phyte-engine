#!/usr/bin/python

import pygame
import gameUtils
import playerUtils
import animation
import move
import physics2d
import engine
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

# initialize pygame
pygame.init()
screen = pygame.display.set_mode(screen_size)
screen.set_alpha(None)
screen.set_colorkey((0,255,255))
pygame.display.set_caption("Fighting Game Engine Test")

done = False

# initialize systems
eng = engine.PygameEngine()
ani = animation.AnimationSystem()
mov = move.MoveSystem()
phy = physics2d.PhysicsSystem()
eng.install_system(ani, (ANIMATIONCOMPLETE,ANIMATIONACTIVATE,
						 ANIMATIONDEACTIVATE))
eng.install_system(mov, (MOVECHANGE,MOVERESET,MOVEACTIVATE,
						 MOVEDEACTIVATE))
eng.install_system(phy, (ADDFORCE,ADDPHYSICSCOMPONENT,
						 REMOVEPHYSICSCOMPONENT))

# Game loop
while not(done):
	last_time = current_time
	current_time = pygame.time.get_ticks()
	time_since_last_update = current_time - last_time

	eng.update(time_since_last_update)