import pygame
import sys
import numpy as np
from utils import *


# pygame setup
pygame.init()
pygame.display.set_caption("Pong-Inertial Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

# Setting fonts
font = pygame.font.SysFont('arial', 40)
title = pygame.font.SysFont('verdana', 150).render('Pong-Inertial', False, (250, 220, 210))

# Adding the musics tracks
music = pygame.mixer.music
music.load("MultiMedia/katyusha_8_bit.mp3")
music.play()

# Scoreboard
P1Score = pygame.font.SysFont('verdana', 40).render(f"Player 1: {player1.score}", False, player1.color)
P2Score = pygame.font.SysFont('verdana', 40).render(f"Player 2: {player1.score}", False, player2.color)

# To run the menu / intro
def run_intro():
    intro = True
    
    # Making the buttons
    startButton = Button(WIDTH/2 - 100, HEIGHT*(1/3+2/10), 200, 50, start, "Start")
    optionButton = Button(WIDTH/2 - 100, HEIGHT*(1/3 + 3/10), 200, 50, options, "Options")
    exitButton = Button(WIDTH/2 - 100, HEIGHT*(1/3 + 4/10), 200, 50, exit, "Exit")
        
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(SURFACE_COLOR)
        screen.blit(title, (WIDTH/2 - title.get_width()/2, HEIGHT*(1/8)))
        startButton.process()
        optionButton.process()
        exitButton.process()
        
        pygame.display.flip()
        clock.tick(FPS)
        
# to run the options page   
def run_options():
    options = True
    
    # making buttons
    menuButton = Button(0, 0, 100, 50, menu, "Menu", False)
    
    while options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(SURFACE_COLOR)
        menuButton.process()
        pygame.display.flip()
        clock.tick(FPS)
        
# to run game
def run_game(screen=screen, clock=clock, running=running, dt=dt):
    music.stop()
    music.load("MultiMedia/Star Wars - Duel Of The Fates 8 - BIT REMIX.mp3")
    music.play()
    
    player1.pos = pygame.Vector2(PLAYER1_POS)
    player2.pos = pygame.Vector2(PLAYER2_POS)
    
    # making buttons
    menuButton = Button(20, 10, 100, 50, leave_game, "Menu", False)
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(SURFACE_COLOR)
        screen.blit(disk, (WIDTH/2-300,HEIGHT/2-300))
        
        screen.blit(P1Score, (WIDTH/2-P1Score.get_width()-40, 20))
        screen.blit(P2Score, (WIDTH/2+40, 20))
        
        # updates buttons
        menuButton.process()

        pygame.draw.rect(screen, player1.color, (player1.pos.x, player1.pos.y, player1.width, player1.height))
        pygame.draw.rect(screen, player2.color, (player2.pos.x, player2.pos.y, player2.width, player2.height))

        keys = pygame.key.get_pressed()

        # player 1 controls
        keys = pygame.key.get_pressed()
        if keys[player1.up]:
            player1.pos.y -= 300 * dt
        if keys[player1.down]:
            player1.pos.y += 300 * dt
        if keys[player1.left]:
            player1.pos.x -= 300 * dt
        if keys[player1.right]:
            player1.pos.x += 300 * dt
            
        # player 2 controls
        if keys[player2.up]:
            player2.pos.y -= 300 * dt
        if keys[player2.down]:
            player2.pos.y += 300 * dt
        if keys[player2.left]:
            player2.pos.x -= 300 * dt
        if keys[player2.right]:
            player2.pos.x += 300 * dt
            
        
        player1.boundary_check()
        player2.boundary_check()
        

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(FPS) / 1000
        

run_intro()
pygame.quit()
sys.exit()