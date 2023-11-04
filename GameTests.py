# Example file showing a circle moving on screen
import pygame
import sys


# Global Variables
SURFACE_COLOR = (50, 50, 50)
WIDTH = 800
HEIGHT = 800
PLAYER1_COLOR = (255, 50, 50)
PLAYER2_COLOR = (50, 255, 50)
FPS = 60


# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
font = pygame.font.SysFont(pygame.font.get_default_font(), 40)



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
                'normal': (200,200,200),
                'hover': (150, 150, 150),
                'pressed': (230, 230, 230),
            }
        else:
            self.textSurf = font.render(text,True, (200, 200, 200))
            self.colors = {
                'normal': SURFACE_COLOR,
                'hover' : SURFACE_COLOR,
                'pressed': (100,100,100)
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
    
# Exit function
def exit():
    pygame.quit()
    sys.exit()
    

def run_game(screen=screen, clock=clock, running=running, dt=dt):
    # making players
    player1 = Player(PLAYER1_COLOR, screen.get_width() / 3, screen.get_height() / 2, 20, 50, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
    player2 = Player(PLAYER2_COLOR, screen.get_width() *2/ 3, screen.get_height() / 2, 30, 10, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
    
    # making buttons
    menuButton = Button(0, 0, 100, 50, menu, "Menu", False)
    restartButton = Button(screen.get_width()/2-50, 0, 100, 50, start, "Restart", False)
    
    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(SURFACE_COLOR)
        
        # updates buttons
        menuButton.process()
        restartButton.process()

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
    startButton = Button(screen.get_width()/2 - 100/2, screen.get_height()/3 - 50/2, 100, 50, start, "Start")
    exitButton = Button(screen.get_width()/2 - 100/2, screen.get_height()*2/3 -50/2, 100, 50, exit, "Exit")
        
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(SURFACE_COLOR)
        startButton.process()
        exitButton.process()
        
        pygame.display.flip()
        clock.tick(FPS)
        # mouse = pygame.mouse.get_pos()
        # for event in pygame.event.get():
        #     if event.type() == pygame.QUIT:
        #         pygame.quit()
        #     elif event.type() == pygame.MOUSEBUTTONDOWN:
        #         pass
                

run_intro()
run_game()
pygame.quit()
sys.exit()