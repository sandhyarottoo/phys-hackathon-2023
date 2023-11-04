#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 14:05:22 2023

@author: sandhya
"""

import pygame
import numpy as np
import sys


####### FUNCTIONS AND CLASSES AND CONSTANT DEFINITIONS ###########

black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)


class CircleSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
    def pos_update(self, dx, dy):
        # Update the position of the sprite by dx and dy
        self.rect.x = dx
        self.rect.y = dy

#time step for euler integration
dt = 0.0001

#accelerations 
def a_radial(w,r,v_theta):
    return -1*(w**2*r+w*v_theta)

def a_tan(w,v_radial,r,ang_acc):
    return w*v_radial+r*ang_acc

#conversion functions
def cartesian_to_polar(pos_xy):
    if pos_xy.x == 0:
        return 0, 0
    r = np.sqrt(pos_xy.x**2+pos_xy.y**2)
    theta = np.arctan(pos_xy.y/pos_xy.x)
    return pygame.Vector2(r, theta)

def polar_to_cartesian(pos_polar):
    x = pos_polar.x*np.cos(pos_polar.y)
    y = pos_polar.x*np.sin(pos_polar.y)
    return pygame.Vector2(x, y)

def update_position(pos_polar,vel_polar,acc_polar):
    pos_polar.x += vel_polar.x*dt
    pos_polar.y += vel_polar.y*dt  

    #update velocity
    vel_polar.x += acc_polar.x*dt
    vel_polar.y -= acc_polar.y*dt
    
    #set a to 0 at each step
    acc_polar.x = 0
    acc_polar.y = 0
    
    #calculate acceleration for next step
    
    acc_polar.y = a_tan(w_platform, vel_polar.x, pos_polar.x, acc_platform)
    acc_polar.x = a_radial(w_platform, pos_polar.x, vel_polar.y)

    return pos_polar,vel_polar,acc_polar



############ MAIN CODE ############

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Create a window
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Circle Sprite")

# Constants
pos_xy = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
BACKGROUND_COLOR = (255, 255, 255)
CIRCLE_COLOR = red

# Create a sprite group
all_sprites = pygame.sprite.Group()

# Create a circle sprite
circle = CircleSprite(pos_xy.x, pos_xy.y, 10, CIRCLE_COLOR)

# Add the circle sprite to the sprite group
all_sprites.add(circle)

# Main game loop
running = True


#initial conditions in polar coords
pos_polar = pygame.Vector2(screen.get_width()/2, np.pi/2)
vel_polar = pygame.Vector2(-300, 0)
acc_polar = pygame.Vector2(0,0)

w_platform = 0.1 #number is in rad/s, returns deg/s
acc_platform = 0 #acceleration of the platform

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #update the positions
    pos_polar,vel_polar,acc_polar = update_position(pos_polar, vel_polar, acc_polar)
    
    #convert positions to cartesian coordinates
    pos_xy = polar_to_cartesian(pos_polar)
    pos_xy.x += screen.get_width()/2
    pos_xy.y += screen.get_height()/2
    
    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    #update the position of the sprite with the calculated acceleration
    circle.pos_update(pos_xy.x,pos_xy.y)
    # Update and draw all sprites
    all_sprites.update()
    all_sprites.draw(screen)

   # Update the display
    pygame.display.flip()
    dt = clock.tick(60) / 1000

# Quit Pygame
pygame.quit()
sys.exit()
