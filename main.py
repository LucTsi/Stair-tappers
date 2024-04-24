# imports
import time
import pygame
import random
import sys


# CONTROLS
#   Esc - PAUSE
#   A/Left Arrow - move left
#   D/Right Arrow - move right
#   Space - reset/start game    


# pygame.init stuff
pygame.init()
pygame.mixer.init()

# music/sounds
pygame.mixer.music.load("ROK.mp3")

# variables and constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # the screen size
player = pygame.Rect((250, 400, 25, 25))  # player
player2 = pygame.Rect((250, 400, 25, 25))
spawn = pygame.Rect((250, 400, 25, 25))  # where the player spawns after death
PLIM = pygame.image.load("plucka.jpg")
PLIM2 = pygame.image.load("plucka.jpg")
LAVA = pygame.image.load("LAVAF.jpg")
BG = pygame.image.load("BGST.jpg")
location = [250, 400]
botton = pygame.Rect((1, 569, 1000, 10))  # the red kill block at the bottom
obstacles_list = []  # list to store obstacles
all_obstacles = []  # list to store all obstacles throughout the game
run = True
dead = False  # are you dead?
playermove1 = 50 #ska vara 50
playermove2 = 62 # ska vara 62
X = 100
Y = 100
X1 = 850
Y2 = 100
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
Pause = False
# Variables to track key pressed
key_a_pressed = False
key_d_pressed = False
key_space_pressed = False
# To see if its the first game
first = True

#functions def
def game_over():  # death function
    global game_over, SPEED, dead, first, Pause
    Save()
    obstacles_list.clear()
    screen.fill((0, 0, 0))
    dead = True
    SPEED = 0
    player.left = spawn.left
    player.top = spawn.top
    first = True
    Pause = False


def wait():  # vet inte faktiskt vill inte ta bort om allt går sönder
    global first, dead, Pause
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                Pause = False


def wating():  # Wait before game and after death
    global SPEED, first
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                SPEED = 3
                first = False


# Function to make the platforms
def new_obs(): #ny platform för att gå på
    global direct
    direction = random.choice(["LEFT", "RIGHT"])
    if direction == "LEFT":
        direct = "LEFT"
        return pygame.Rect((player.left - playermove2, player.top - playermove1, 41, 9))# plr.left = 62   plr.top = 50, har valt dessa nummer eftersom det blir jämnt
    elif direction == "RIGHT":
        direct = "RIGHT"
        return pygame.Rect((player.left + playermove1, player.top - playermove1, 41, 9))# plr.left = 50   plr.top = 50, har valt dessa nummer eftersom det blir jämnt


def Save(): # saves score and highscore
    global Score

    try:
        with open('HighScore.txt', 'r') as r:
            Check = r.readline().strip()
            if Check == "":
                Check = 0
            else:
                Check = int(Check)

        if Score > Check:
            with open('HighScore.txt', 'w') as f:
                f.write(str(Score))
    except FileNotFoundError:

        with open('HighScore.txt', 'w') as f:
            f.write(str(Score))

def GoUp():
    global spedd
    if Pause == False:
        SPEED = spedd + 0.0005
        spedd = SPEED

    if Pause == False:
        player.top += SPEED
    elif Pause == True:
        player.top += 0

    if Pause == False:
        for obs in obstacles_list:
            obs.top += SPEED
    elif Pause == True:
        for obs in obstacles_list:
            obs.top += 0

def DispScreen(): #displays och draw allt på skärmen
    screen.fill((0, 0, 0))  # Draw background after updating player position
    #game visuals
    screen.blit(BG, [1, 1])
    pygame.draw.rect(screen, (0, 0, 0), player)
    screen.blit(PLIM, player)
    pygame.draw.rect(screen, (0, 0, 0), botton)
    screen.blit(LAVA, botton)
    #texts och score displays
    with open('HighScore.txt', 'r') as l:
        checking = l.readline()
    high = font.render(str(checking), True, blue)
    text = font.render(str(Score), True, green)
    screen.blit(text, textRect)
    screen.blit(high, TextRect2)
    #obs display
    for obs in obstacles_list:
        pygame.draw.rect(screen, (255, 255, 255), obs)
    #makes screen black while pausing
    if Pause == True:  # makes screen black to avoid cheating
        screen.fill((0, 0, 0))

# The game loop
while run:
    if first:  # specific stuff to happen when you just enter the game
        pygame.mixer.music.stop()
        obstacles_list.append(pygame.Rect((player.left - 62, player.top - 50, 41, 9)))
        direct = "LEFT"
        SPEED = 0
        spedd = 1
        score = 0
        wating()
        Pause = False
        font = pygame.font.Font('freesansbold.ttf', 32)
        Score = 0
        text = font.render(str(Score), True, green, blue)
        TextRect2 = text.get_rect()
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)
        TextRect2.center = (X1 // 2, Y2 // 2)
        pygame.mixer.music.play(loops=-1, start=1, fade_ms=2000)
        first = False
        screen.fill((0, 0, 0))
        Pause = False
        first = False


    for event in pygame.event.get():  # quit
        if event.type == pygame.QUIT:
            run = False

#DEATH
    #kills the player at the botton
    if player.colliderect(botton):
        game_over()

# MOVEMENT

    # check the key pressed
    keys = pygame.key.get_pressed()

    # Check for A or Larrow key press
    if (keys[pygame.K_LEFT] and not key_a_pressed and not Pause) or (
            keys[pygame.K_a] and not key_a_pressed and not Pause):
        if direct == "LEFT":
            player.left = obstacles_list[-1].left + 8
            player.top = obstacles_list[-1].top - 25
            Move = 54 #54
            Score += 1  # Simplified Score increment
            player.left += Move  # moves everything to the right
            for obs in obstacles_list:  # moves everything to the right
                obs.left += Move
            obstacles_list.append(new_obs())
            key_a_pressed = True
        elif direct == "RIGHT":
            game_over()
            print("dead")
    elif not keys[pygame.K_LEFT] and not keys[pygame.K_a]:
        key_a_pressed = False

    # Check for D or Rarrow key press
    if (keys[pygame.K_RIGHT] and not key_d_pressed and not Pause) or (
            keys[pygame.K_d] and not key_d_pressed and not Pause):
        if direct == "RIGHT":
            player.left = obstacles_list[-1].left + 8
            player.top = obstacles_list[-1].top - 25
            Move = 58 # 58
            Score += 1  # Simplified Score increment
            player.left -= Move  # moves everything to the right
            for obs in obstacles_list:
                obs.left -= Move  # moves everything to the right
            obstacles_list.append(new_obs())
            key_d_pressed = True
        elif direct == "LEFT":
            game_over()
            print("dead")
    elif not keys[pygame.K_RIGHT] and not keys[pygame.K_d]:
        key_d_pressed = False

# Pause Functions

    if keys[pygame.K_ESCAPE] and not key_space_pressed and first == False:
        print("space")
        if Pause == False:
            print("paused")
            Pause = True
            key_space_pressed = True
        elif Pause == True:
            print("unpause")
            Pause = False
            key_space_pressed = True
    elif not keys[pygame.K_ESCAPE]:
        key_space_pressed = False

#VISUALS

    GoUp() # makes the camera go up

    DispScreen() #draws everything on screen
    # die if the player touches the red line at the botton


#OTHERS

    # Update the display
    pygame.display.update()

    # Append obstacles to the all_obstacles list
    all_obstacles.extend(obstacles_list)

    # Cap the frame rate
    pygame.time.Clock().tick(100)
    Save()# saves score

pygame.display.update()
pygame.quit()