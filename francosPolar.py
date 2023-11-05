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

BACKGROUND_COLOR = (255, 255, 255)
CIRCLE_COLOR = red

#screen width and height
width = 790
height = 790
RING_RADIUS = 300
PLAYER_RADIUS = 305

PLAYER_VELOCITY = 10
PLAYER_ARC_ANGLE = np.pi / 12  # 90 degrees in radians

player1_angle = -np.pi / 2
player2_angle = -np.pi / 2

#time step for euler integration
dt = 0.0001

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

#accelerations 
def a_radial(w,r,v_theta):
    return -1*(w**2*r+w*v_theta)

def a_tan(w,v_radial,r,ang_acc):
    return w*v_radial+r*ang_acc

class Player(pygame.sprite.Sprite):
    def __init__(self, color, start_angle, keys):
        super().__init__()
        self.score = 0
        self.color = color
        self.pos = pygame.Vector2(PLAYER_RADIUS, start_angle)
        self.keys = keys
        player_width = 8
        
        self.image = pygame.Surface((2*(PLAYER_RADIUS) , 2*(PLAYER_RADIUS)), pygame.SRCALPHA)
        pygame.draw.arc(self.image, self.color,
                        (0, 0, (PLAYER_RADIUS) * 2, (PLAYER_RADIUS) * 2), 
                        self.pos.y - PLAYER_ARC_ANGLE / 2,
                        self.pos.y + PLAYER_ARC_ANGLE / 2,
                        width=player_width)
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
    
    def update(self, keys):
        
        # Move the player on the ring
        if keys[self.keys[0]]:
            self.pos.y -= PLAYER_VELOCITY*dt  
        if keys[self.keys[1]]:
            self.pos.y += PLAYER_VELOCITY*dt   


class PointCharge(pygame.sprite.Sprite):
    def __init__(self, pos, strength):
        super().__init__()
        self.pos = pos
        self.strength = strength
        self.radius = 15

        self.image = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color("blue"), (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()

        pos_cartesian = polar_to_cartesian(self.pos)
        self.rect.center = (pos_cartesian.x + width/2, pos_cartesian.y + height/2)

    def computeForce(self, other_pos):

        direction_vec = self.pos - other_pos
        distance = direction_vec.length()
        direction_vec = direction_vec/distance
        
        return (self.strength/distance**2)*direction_vec


class CircleSprite(pygame.sprite.Sprite):
# pos, vel and acc are in polar
    def __init__(self, pos, vel, acc, radius, color):
        super().__init__()
        self.pos = pos
        self.vel = vel
        self.acc = acc

        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()

        pos_cartesian = polar_to_cartesian(self.pos)
        self.rect.center = (pos_cartesian.x, pos_cartesian.y)
    
    def getForce(self, sources):
        #each object in sources must have a computeForce(self.pos, other.pos) method
        force = pygame.Vector2(0, 0)

        force.y += a_tan(w_platform, self.vel.x, self.pos.x, acc_platform)
        force.x += a_radial(w_platform, self.pos.x, self.vel.y)
        #could add friction

        for source in sources:
            force += source.computeForce(self.pos)

        return force

        
    def update(self, force_sources):
        # Update the position of the sprite
        self.pos += self.vel*dt
        self.vel += self.acc*dt

        self.acc *= 0
        self.acc += self.getForce(force_sources)

        pos_cartesian = polar_to_cartesian(self.pos)
        self.rect.center = (pos_cartesian.x + width/2, pos_cartesian.y + height/2)


############ MAIN CODE ############

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((790,790))
pygame.display.set_caption("Circle Sprite")

#initial conditions in polar coords
pos_polar = pygame.Vector2(screen.get_width()/2, np.pi/2)
vel_polar = pygame.Vector2(-300, 0)
acc_polar = pygame.Vector2(0,0)

# Create a sprite
circle = CircleSprite(pos_polar, vel_polar, acc_polar, 10, CIRCLE_COLOR)
circles = pygame.sprite.Group()
circles.add(circle)

# create a point charge
charge = PointCharge(pygame.Vector2(-100, 0), 100000)
charges = pygame.sprite.Group()
charges.add(charge)

# players
player1_keys = [pygame.K_a, pygame.K_d]
player2_keys = [pygame.K_LEFT, pygame.K_RIGHT]

player1 = Player("blue", 0, player1_keys)
player2 = Player("red", np.pi, player2_keys)
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

# Main game loop
running = True

w_platform = 0.01 #number is in rad/s, returns deg/s
acc_platform = 0 #acceleration of the platform

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.circle(screen, (160,160,160), (width / 2, height / 2), RING_RADIUS)

    circles.update(charges)
    circles.draw(screen)

    charges.draw(screen)
    
    keys = pygame.key.get_pressed()
    players.update(keys)
    players.draw(screen)
    
   # Update the display
    pygame.display.flip()
    dt = clock.tick(60) / 1000

# Quit Pygame
pygame.quit()
sys.exit()