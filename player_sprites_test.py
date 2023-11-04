#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  4 17:11:01 2023

@author: sandhya
"""


import pygame
import numpy as np
import sys


####### FUNCTIONS AND CLASSES AND CONSTANT DEFINITIONS ###########
SCREEN_WIDTH,SCREEN_HEIGHT = 500,500
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

RING_RADIUS = 300
PLAYER_RADIUS = 305

PLAYER1_VELOCITY = 0.05
PLAYER2_VELOCITY = 0.05
PLAYER1_ARC_ANGLE = np.pi / 9  # 90 degrees in radians
PLAYER2_ARC_ANGLE = np.pi / 9  # 90 degrees in radians

# Player position and angle (starts at the top of the ring)
player1_angle = -np.pi / 2  # -90 degrees in radians
player1_x = SCREEN_WIDTH // 2 + RING_RADIUS * np.cos(player1_angle)
player1_y = SCREEN_HEIGHT // 2 + RING_RADIUS * np.sin(player1_angle)
player2_angle = -np.pi / 2  # -90 degrees in radians
player2_x = SCREEN_WIDTH // 2 + RING_RADIUS * np.cos(player2_angle)
player2_y = SCREEN_HEIGHT // 2 + RING_RADIUS * np.sin(player2_angle)


class CircleSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color):
        super().__init__()
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        
    def pos_update(self, x_new, y_new):
        # Update the position of the sprite by dx and dy
        self.rect.x = x_new
        self.rect.y = y_new
        
    def checkCollision(self, sprite1, sprite2):
        col = pygame.sprite.collide_rect(sprite1, sprite2)
        if col == True:
            sys.exit()
            
class Player(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface((PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.arc(self.image, color, (0, 0, PLAYER_RADIUS * 2, PLAYER_RADIUS * 2), 0, PLAYER1_ARC_ANGLE, width=5)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self,right_left,velocity,ring_radius,angle):
        keys = pygame.key.get_pressed()
        if right_left == 'ad':
            if keys[pygame.K_a]:
                angle -= velocity * ring_radius
            if keys[pygame.K_d]:
                angle += velocity*ring_radius
        if right_left == 'arrows':
            if keys[pygame.K_LEFT]:
                angle -= velocity * ring_radius
            if keys[pygame.K_RIGHT]:
                angle += velocity*ring_radius
        
        self.rect.x = (SCREEN_WIDTH // 2 + ring_radius * np.cos(angle))-PLAYER_RADIUS
        self.rect.y = (SCREEN_WIDTH // 2 + ring_radius * np.sin(angle)) -PLAYER_RADIUS
    
        
        



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
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Circle Sprite")

# Constants
pos_xy = pygame.Vector2(screen.get_width()/2,screen.get_height()/2)
BACKGROUND_COLOR = (255, 255, 255)

# Create a sprite group
all_sprites = pygame.sprite.Group()

# Create a circle sprite

CIRCLE_COLOR = red

circle = CircleSprite(pos_xy.x, pos_xy.y, 10, CIRCLE_COLOR)

player1 = Player(blue,player1_x,player1_y)
player2 = Player(red,player2_x,player2_y)



# Add the circle sprite to the sprite group
all_sprites.add(circle,player1,player2)

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
    player1.update('ad',PLAYER1_VELOCITY,RING_RADIUS,player1_angle)
    player2.update('arrows',PLAYER2_VELOCITY,RING_RADIUS,player2_angle)
    
    # Update and draw all sprites
    all_sprites.draw(screen)

   # Update the display
    pygame.display.flip()
    dt = clock.tick(60) / 1000

# Quit Pygame
pygame.quit()
sys.exit()
