# imports
import time
import pygame
import random
import sys
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
spawn = pygame.Rect((250, 400, 25, 25))  # where the player spawns after death
PLIM = pygame.image.load("PLAYERMAN.jpg")
LAVA = pygame.image.load("LAVAF.jpg")
BG = pygame.image.load("BGST.jpg")
location = [250, 400]
botton = pygame.Rect((1, 569, 1000, 10))  # the red kill block at the bottom
obstacles_list = []  # list to store obstacles
all_obstacles = []  # list to store all obstacles throughout the game
run = True
dead = False  # are you dead?
X = 100
Y = 100
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

def game_over():  # death function
    global game_over, SPEED, dead, first
    obstacles_list.clear()
    screen.fill((0, 0, 0)) 
    dead = True
    SPEED = 0
    player.left = spawn.left
    player.top = spawn.top
    first = True

def wait(): # vet inte faktiskt vill inte ta bort om allt går sönder
    global first, dead
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.left = spawn.left
                player.top = spawn.top
                waiting = False
                screen.fill((0, 0, 0))
                first = True
                dead = False

def wating(): # Wait before game and after death
    global SPEED
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                SPEED = 3
# Function to make the platforms
def new_obs():
    global direct
    direction = random.choice(["LEFT", "RIGHT"])
    if direction == "LEFT":
        direct = "LEFT"
        return pygame.Rect((player.left - 62, player.top - 50, 41, 9))
    elif direction == "RIGHT":
        direct = "RIGHT"
        return pygame.Rect((player.left + 50, player.top - 50, 41, 9))

# Variables to track key pressed
key_a_pressed = False
key_d_pressed = False

# To see if its the first game
first = True

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
        font = pygame.font.Font('freesansbold.ttf', 32)
        Score = 0
        text = font.render(str(Score), True, green, blue)
        textRect = text.get_rect()
        textRect.center = (X // 2, Y // 2)
        pygame.mixer.music.play(loops=-1, start=1, fade_ms=2000)
        first = False
        screen.fill((0, 0, 0))

        
    for event in pygame.event.get():  # quit
        if event.type == pygame.QUIT:
            run = False

    # check the key pressed
    keys = pygame.key.get_pressed()

    # die if the player touches the red line at the botton
    if player.colliderect(botton):
        game_over()

    # Check for A key press
    if keys[pygame.K_LEFT] and not key_a_pressed:
        if direct == "LEFT":
            player.left = obstacles_list[-1].left + 8
            player.top = obstacles_list[-1].top - 25
            Move = 54
            Score = Score + 1
            player.left += Move     # moves everything to the right
            for obs in obstacles_list:  # moves everything to the right
                obs.left += Move
            obstacles_list.append(new_obs())
            key_a_pressed = True
        elif direct == "RIGHT":
            game_over()
            print("dead")
    elif not keys[pygame.K_LEFT]:
        key_a_pressed = False

    # Check for D key press
    if keys[pygame.K_RIGHT] and not key_d_pressed:
        if direct == "RIGHT":
            player.left = obstacles_list[-1].left + 8
            player.top = obstacles_list[-1].top - 25
            Move = 58
            Score = Score + 1
            player.left -= Move   # moves everything to the right

            for obs in obstacles_list:
                obs.left -= Move    # moves everything to the right
            obstacles_list.append(new_obs())
            key_d_pressed = True
        elif direct == "LEFT":
            game_over()
            print("dead")
    elif not keys[pygame.K_RIGHT]:
        key_d_pressed = False
    # makes the game move down and becomes faster every sec
    SPEED = spedd + 0.0005
    spedd = SPEED


    player.top += SPEED
    for obs in obstacles_list:
        obs.top += SPEED


    screen.fill((0, 0, 0))  # Draw background after updating player position
    screen.blit(BG, [1, 1])
    pygame.draw.rect(screen, (0, 0, 0), player)
    screen.blit(PLIM, player)
    pygame.draw.rect(screen, (0, 0, 0), botton)
    screen.blit(LAVA, botton)
    text = font.render(str(Score), True, green)
    screen.blit(text, textRect)
    for obs in obstacles_list:
            pygame.draw.rect(screen, (255, 255, 255), obs)


    # Update the display
    pygame.display.update()

    # Append obstacles to the all_obstacles list
    all_obstacles.extend(obstacles_list)

    # Cap the frame rate
    pygame.time.Clock().tick(100)

# At the end of the game loop, you can draw all obstacles
for obs in all_obstacles:
      pygame.draw.rect(screen, (255, 255, 255), obs)
pygame.display.update()


pygame.quit()
