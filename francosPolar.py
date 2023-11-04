import pygame
import numpy as np
from pygame.locals import *
import pygame.examples.moveit
import pygame.sprite

black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)

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
    
slaying = True

#define initial game conditions
screen_size = screen_width, screen_height = 790, 790
screen = pygame.display.set_mode(screen_size)

clock = pygame.time.Clock()
fps_limit = 60

#initial conditions (in cartesian coords):
pos_xy = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

#in polar coords
pos_polar = pygame.Vector2(screen.get_width()/2, np.pi/2)
vel_polar = pygame.Vector2(-300, 0)
acc_polar = pygame.Vector2(0,0)

w_platform = 0.1 #number is in rad/s, returns deg/s
acc_platform = 0 #acceleration of the platform

#make the circle
colorcircle = (red)
circle_radius = 20
circle = pygame.draw.circle(screen, colorcircle, pos_xy, circle_radius)

while slaying:
    clock.tick(fps_limit)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            slaying = False  
    
    #update position
    pos_polar.x += vel_polar.x*dt
    pos_polar.y += vel_polar.y*dt  
    #change the position to cartesian
    pos_xy = polar_to_cartesian(pos_polar)
    pos_xy.x += screen.get_width()/2
    pos_xy.y += screen.get_height()/2

    #update velocity
    vel_polar.x += acc_polar.x*dt
    vel_polar.y += acc_polar.y*dt
    
    #set a to 0 at each step
    acc_polar.x = 0
    acc_polar.y = 0
    
    #calculate acceleration for next step
    
    acc_polar.y = a_tan(w_platform, vel_polar.x, pos_polar.x, acc_platform)
    acc_polar.x = a_radial(w_platform, pos_polar.x, vel_polar.y)
            
    #screen.fill(white)

    #update circle position 
    circle = pygame.draw.circle(screen, colorcircle, pos_xy, circle_radius)
    
    
    pygame.display.flip()
    dt = clock.tick(60) / 1000
    
pygame.quit()