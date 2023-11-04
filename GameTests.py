# Example file showing a circle moving on screen
import pygame
import sys


# Global Variables
SURFACE_COLOR = (50, 50, 60)
WIDTH = 1200
HEIGHT = 800
PLAYER1_COLOR = (255, 50, 50)
PLAYER2_COLOR = (50, 255, 50)
FPS = 60


# pygame setup
pygame.init()
pygame.display.set_caption("Pong-Inertial Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont(pygame.font.get_default_font(), 40)
title = pygame.font.SysFont('verdana', 150).render('Pong-Inertial', False, (250, 220, 210))


class Player():
    def __init__(self,color, x, y, width, height, up, down, left, right, radius=20):
        self.pos = pygame.Vector2(x, y)
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.radius = radius
        self.width = width
        self.height = height
        self.color = color
        
    def boundary_check(self, width=screen.get_width(), height=screen.get_height()):
        if self.pos.x + self.radius >= width:
            self.pos.x = width - self.radius
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            
        if self.pos.y + self.radius >= height:
            self.pos.y = height - self.radius
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            
class Button():
    def __init__(self, x, y, width, height, function=None, text="Button",inMenu=True , font=font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.function = function
        
        
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if inMenu:
            self.textSurf = font.render(text,True, (40, 40, 40))
            self.colors = {
                'normal': (196,164,132),
                'hover': (156, 124, 92),
                'pressed': (220, 220, 220),
            }
        else:
            self.textSurf = font.render(text,True, (200, 200, 200))
            self.colors = {
                'normal': SURFACE_COLOR,
                'hover' : SURFACE_COLOR,
                'pressed': (130,130,130)
            }
        
    def process(self):
        mouse = pygame.mouse
        mousePos = mouse.get_pos()
        self.surface.fill(self.colors['normal'])
        if self.rect.collidepoint(mousePos):
            self.surface.fill(self.colors['hover'])
            if mouse.get_pressed(num_buttons=3)[0]:
                self.surface.fill(self.colors['pressed'])
                self.function()
                
        self.surface.blit(self.textSurf, [self.rect.width/2 - self.textSurf.get_rect().width/2, 
                                                self.rect.height/2 - self.textSurf.get_rect().height/2])
        screen.blit(self.surface, self.rect)
        
 
# Start function
def start():
    run_game()
    
# Opens intro page
def menu():
    run_intro()    
    
def options():
    run_options()
    
# Exit function
def exit():
    pygame.quit()
    sys.exit()
    
center_width = screen.get_width()/2
center_height = screen.get_height()/2
    
    
disk = pygame.image.load("MultiMedia/TableTop.png").convert_alpha()
disk = pygame.transform.scale(disk, (600, 600))

def run_game(screen=screen, clock=clock, running=running, dt=dt):
    # making players
    player1 = Player(PLAYER1_COLOR, WIDTH / 3, HEIGHT / 2, 20, 50, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
    player2 = Player(PLAYER2_COLOR, WIDTH *2/ 3, HEIGHT / 2, 30, 10, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
    
    # making buttons
    menuButton = Button(0, 0, 100, 50, menu, "Menu", False)
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(SURFACE_COLOR)
        screen.blit(disk, (WIDTH/2-300,HEIGHT/2-300))
        
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
        
        
def run_intro(screen=screen):
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
                
                
def run_options(screen=screen):
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
        
    

run_intro()
pygame.quit()
sys.exit()