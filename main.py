import pygame
import numpy as np
import sys
import os

# global player2_score = 0
# global player1_score = 0
# global max_score = 10





########## CONSTANTS ##########

# Constants
WIDTH = 1200
HEIGHT = 800
FPS = 60
MAXSCORE = 10
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
white = (255,255,255)
SURFACE_COLOR = (50, 50, 60)
PLAYER1_COLOR = (255, 50, 50)
PLAYER2_COLOR = (50, 50, 255)
DISK_RADIUS = 300
PLAYER_RADIUS = 305
PLAYER_WIDTH = 8
CIRCLE_COLOR = red
W_PLATFORM = 0.0015 # number is in rad/s, returns deg/s
ACC_PLATFORM = 0
V_INITIAL = -300
PLAYER_VELOCITY = 4
PLAYER_ARC_ANGLE = np.pi / 12  # 90 degrees in radians
MAX_SCORE = 2

player1_angle = -np.pi / 2
player2_angle = -np.pi / 2

#time step for euler integration
dt = 0.0001






########## FUNCTIONS ##########

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








########## CLASSES ##########

class Player(pygame.sprite.Sprite):
    def __init__(self, color, start_angle, keys):
        super().__init__()
        self.score = 0
        self.color = color
        self.pos = pygame.Vector2(PLAYER_RADIUS, start_angle)
        self.keys = keys
        
        self.image = pygame.Surface((2*(PLAYER_RADIUS) , 2*(PLAYER_RADIUS)), pygame.SRCALPHA)
        pygame.draw.arc(self.image, self.color,
                        (0, 0, (PLAYER_RADIUS) * 2, (PLAYER_RADIUS) * 2), 
                        self.pos.y - PLAYER_ARC_ANGLE / 2,
                        self.pos.y + PLAYER_ARC_ANGLE / 2,
                        width=PLAYER_WIDTH)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
    
    def update(self, keys):
        
        # Move the player on the ring
        if keys[self.keys[0]]:
            self.pos.y -= PLAYER_VELOCITY*dt  
        if keys[self.keys[1]]:
            self.pos.y += PLAYER_VELOCITY*dt  

        self.image.fill(pygame.SRCALPHA)
        pygame.draw.arc(self.image, self.color,
                        (0, 0, (PLAYER_RADIUS) * 2, (PLAYER_RADIUS) * 2), 
                        self.pos.y - PLAYER_ARC_ANGLE / 2,
                        self.pos.y + PLAYER_ARC_ANGLE / 2,
                        width=PLAYER_WIDTH) 



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
        self.rect.center = (pos_cartesian.x + WIDTH/2, pos_cartesian.y + HEIGHT/2)

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
        self.radius = radius
        self.bool_color = False
        self.color = PLAYER1_COLOR

        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()

        pos_cartesian = polar_to_cartesian(self.pos)
        self.rect.center = (pos_cartesian.x, pos_cartesian.y)
        
        self.respawn = False
    
    def getForce(self, sources):
        #each object in sources must have a computeForce(self.pos, other.pos) method
        force = pygame.Vector2(0, 0)

        force.y += a_tan(W_PLATFORM, self.vel.x, self.pos.x, ACC_PLATFORM)
        force.x += a_radial(W_PLATFORM, self.pos.x, self.vel.y)
        #could add friction

        for source in sources:
            force += source.computeForce(self.pos)

        return force

        
    def update(self, force_sources,player1,player2):
        
        self.respawn = False

        if pygame.sprite.collide_mask(self,player1) or pygame.sprite.collide_mask(self,player2):
            
            self.bool_color = not self.bool_color

            #collision change of motion
            if self.pos.x < 0:
                self.pos.x = -(PLAYER_RADIUS - PLAYER_WIDTH - self.radius)
            else:
                self.pos.x = (PLAYER_RADIUS - PLAYER_WIDTH - self.radius)
            
            if abs(self.vel.x) < 50 or abs(self.vel.y) > 50:
                self.vel.x *= -1.25
                self.vel.y *= 0.8
            else:
                self.vel.x *= -1.08
        
        # Update the position of the sprite
        self.pos += self.vel*dt
        self.vel += self.acc*dt

        self.acc *= 0
        self.acc += self.getForce(force_sources)

        pos_cartesian = polar_to_cartesian(self.pos)
        
        self.rect.center = (pos_cartesian.x + WIDTH/2, pos_cartesian.y + HEIGHT/2)

        if self.bool_color:
            self.color = PLAYER1_COLOR
        else:
            self.color = PLAYER2_COLOR
            
        #when the ball leaves the disk
        if abs(self.pos.x) > PLAYER_RADIUS+PLAYER_WIDTH and player1.score < MAX_SCORE and player2.score < MAX_SCORE:
            if self.color == PLAYER1_COLOR:
                player2.score += 1
            else:
                player1.score += 1
            self.respawn = True

        

        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
      
            
            
class Button():
    def __init__(self, x, y, width, height, function, text, font, inMenu=True ):
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
        



class scoreboard():
    def __init__(self,player1,player2):
        # Scoreboard setup
        self.P1Score = pygame.font.SysFont('verdana', 40).render(f"Player 1: {player1.score}", False, player1.color)
        self.P2Score = pygame.font.SysFont('verdana', 40).render(f"Player 2: {player2.score}", False, player2.color)

    def update_score(self):
        self.P1Score = pygame.font.SysFont('verdana', 40).render(f"Player 1: {player1.score}", False, player1.color)
        self.P2Score = pygame.font.SysFont('verdana', 40).render(f"Player 2: {player2.score}", False, player2.color)







########## GAME ##########

# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("Pong-Inertial Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Setting fonts
font = pygame.font.SysFont('arial', 40)
title = pygame.font.SysFont('verdana', 150).render('Pong-Inertial', False, (250, 220, 210))

# Adding the musics tracks
music = pygame.mixer.music
music.load("/Users/sandhya/phys-hackathon-2023/MultiMedia/katyusha_8_bit.mp3")
music.play(loops=-1) # -1 loops music indefinitely

#initial conditions in polar coords
pos_polar = pygame.Vector2(DISK_RADIUS*np.random.randint(5,10)/10, np.pi/2)
vel_polar = pygame.Vector2(V_INITIAL, 0)
acc_polar = pygame.Vector2(0,0)

# Create a sprite
circle = CircleSprite(pos_polar, vel_polar, acc_polar, 20, CIRCLE_COLOR)
circles = pygame.sprite.Group()
circles.add(circle)

# Create disk (table top)
disk = pygame.image.load("/Users/sandhya/phys-hackathon-2023/MultiMedia/TableTop.png").convert_alpha()
disk = pygame.transform.scale(disk, (DISK_RADIUS*2, DISK_RADIUS*2))

# create a point charge
# charge = PointCharge(pygame.Vector2(-100, 0), 100000)
charges = pygame.sprite.Group()
# charges.add(charge)

# Players
player1_keys = [pygame.K_d, pygame.K_a]
player2_keys = [pygame.K_RIGHT, pygame.K_LEFT]

player1 = Player(PLAYER1_COLOR, 0, player1_keys)
player2 = Player(PLAYER2_COLOR, np.pi, player2_keys)
players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

# Scoreboard setup
P1Score = pygame.font.SysFont('verdana', 40).render(f"Player 1: {player1.score}", False, player1.color)
P2Score = pygame.font.SysFont('verdana', 40).render(f"Player 2: {player1.score}", False, player2.color)

scoreboard = scoreboard(player1,player2)

# Starts function
def start():
    run_game()
    
# returns to menu / intro page
def leave_game():
    music.load("/Users/sandhya/phys-hackathon-2023/MultiMedia/katyusha_8_bit.mp3")
    music.play(loops=-1) # -1 loops music indefinitely
    run_intro() 

# Opens intro page
def menu():
    run_intro()    
    
# Opens options
def options():
    run_options()
    
# Exits function
def exit():
    pygame.quit()
    sys.exit()

####### UI FUNCTION & GAMEPLAY ########

# To run the menu / intro
def run_intro():
    intro = True
    
    # Making the buttons
    startButton = Button(WIDTH/2 - 100, HEIGHT*(1/3+2/10), 200, 50, start, "Start", font)
    optionButton = Button(WIDTH/2 - 100, HEIGHT*(1/3 + 3/10), 200, 50, options, "Options", font)
    exitButton = Button(WIDTH/2 - 100, HEIGHT*(1/3 + 4/10), 200, 50, exit, "Exit", font)
        
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
    menuButton = Button(20, 10, 100, 50, menu, "Menu", font, False)
    
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
def run_game():
    global dt
    # organize music
    music.stop()
    music.load("/Users/sandhya/phys-hackathon-2023/MultiMedia/Star Wars - Duel Of The Fates 8 - BIT REMIX.mp3")
    music.play(loops=-1) # -1 loops music indefinitely
    
    # reset initial player and circle positions
    player1.pos[1] = 0
    player2.pos[1] = np.pi
    circle.pos = pygame.Vector2(DISK_RADIUS/10, np.random.sample()*np.pi/2)
    circle.vel = vel_polar*np.random.sample()
    circle.acc = acc_polar


    
    # making buttons
    menuButton = Button(20, 10, 100, 50, leave_game, "Menu", font, False)
    
    # starting main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                

        # Clears the screen
        screen.fill(SURFACE_COLOR)
        screen.blit(disk, (WIDTH/2-300,HEIGHT/2-300))
        
        # updates buttons
        menuButton.process()

        circles.update(charges,player1,player2)
        circles.draw(screen)

        charges.draw(screen)
        
        keys = pygame.key.get_pressed()
        players.update(keys)
        players.draw(screen)
        
        scoreboard.update_score()
        screen.blit(scoreboard.P1Score, (WIDTH/2-scoreboard.P1Score.get_width()-40, 20))
        screen.blit(scoreboard.P2Score, (WIDTH/2+40, 20))
        
        text_time = 0
        game_over = False
        current_time = pygame.time.get_ticks()
        if player1.score == MAX_SCORE:
            text = font.render("Congratulations Player 1!",False, black)
            text_time = current_time + 2000
            game_over = True
            circle.respawn = False
        if player2.score == MAX_SCORE:
            text = font.render("Congratulations Player 2!",False, black)
            text_time = current_time + 2000
            game_over = True
            circle.respawn = False
        if circle.respawn:
            text_time = current_time + 2000
            text = pygame.font.SysFont('verdana', 40).render('Respawning in 2 seconds...', True, black)
        while pygame.time.get_ticks() < text_time:
            screen.blit(text, text.get_rect(center = screen.get_rect().center))
            circle.pos = pygame.Vector2(PLAYER_RADIUS/10,np.random.sample()*2*np.pi)
            circle.vel = pygame.Vector2(np.random.sample()*100,np.random.sample()*10)
            pygame.display.update()
        if game_over:
            menu()

                
            
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        dt = clock.tick(FPS) / 1000
        

run_intro()
pygame.quit()
sys.exit()