### Yo yo yo ###

import numpy as np
import matplotlib.pyplot
import pygame
import sys

def applyForce(acc, mass, forces):
    #takes a list of force vectors and returns an updated acceleration
    for force in forces:
        acc += force/mass
    
    return acc

def gravForce(mass):
    g = 1700
    return pygame.Vector2(0, mass*g)


def main():
     
    # pygame setup
    pygame.init()
    width = 1280
    height = 820
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    running = True
    dt = 0.01
    

    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    player_vel = pygame.Vector2(0, 0)
    player_acc = pygame.Vector2(0, 0)
    player_mass = 200
    speed = 600

    gravity = False

    ground_height = 50
    ground_boundary = height - ground_height
    ground = pygame.Rect(0, ground_boundary, width, ground_height)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # "Do something" only once per key press
                    gravity = not gravity

        # fill the screen with a color to wipe away anything from last frame
        
        screen.fill("lightblue")

        radius = 40
        pygame.draw.circle(screen, "black", player_pos, radius)
        pygame.draw.rect(screen, "brown", ground)

        forces = []
        
        if gravity:
            
            if (player_pos.x >= width - radius):
                player_pos.x = width - radius
                player_vel.x *= -1
            elif (player_pos.x <= radius):
                player_pos.x = radius
                player_vel.x *= -1

            if player_pos.y >= ground_boundary - radius:
                player_pos.y = ground_boundary - radius
                
                player_vel.y *= -1

            forces.append(gravForce(player_mass))
            player_pos += player_vel*dt
            player_vel += player_acc*dt

            player_acc.x = 0
            player_acc.y = 0
            player_acc = applyForce(player_acc, player_mass, forces)


        else:
            keys = pygame.key.get_pressed()
            player_vel.x = 0
            player_vel.y = 0
            if keys[pygame.K_w]:
                player_vel.y = -speed
                player_pos.y += player_vel.y * dt
            if keys[pygame.K_s]:
                player_vel.y = speed
                player_pos.y += player_vel.y * dt
            if keys[pygame.K_a]:
                player_vel.x = -speed
                player_pos.x += player_vel.x * dt
            if keys[pygame.K_d]:
                player_vel.x = speed
                player_pos.x += player_vel.x * dt
        


        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()
    sys.exit()



main()