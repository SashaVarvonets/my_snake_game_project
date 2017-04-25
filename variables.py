import pygame, random, time, os
from pygame.locals import * 
pygame.init()

# Window options
window_width = 600
window_height = 400
# Image1 = pygame.image.load(os.path.join('image','image2.jpg'))

snake_size = 20
assert window_width % snake_size == 0, "Window width must be a multiple of cell size."
assert window_height % snake_size == 0, "Window height must be a multiple of cell size."
window_width_size = int(window_width / snake_size)
window_height_size = int(window_height / snake_size)


# Food options
food_spawn = False
great_food_spawn = False
great_food_pos = [0,0]
apple1_image = pygame.image.load(os.path.join('image','apple1.png'))
apple2_image = pygame.image.load(os.path.join('image','apple2.png'))
apple_red_20 = pygame.image.load(os.path.join('image','yabloko20na20.png'))
apple_black_20 = pygame.image.load(os.path.join('image','apple20na20 .png'))

# Colors RGB
red = pygame.Color(255,0,0) # Gameover
green = pygame.Color(0,255,0) #Snake body
dark_green = pygame.Color(0,100,0) #Snake head
black = pygame.Color(0,0,0) #Score and level
white = pygame.Color(240,255,255) #Background
brown = pygame.Color(165,42,42) #Food
grey = pygame.Color(40,40,40) # Border

# Speed and level options
speed = 5
score = 0
rate = 0
level = 1
RUNNING, PAUSE = 0, 1
state = RUNNING