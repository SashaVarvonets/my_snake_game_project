import pygame, random, time, os
from pygame.locals import * 
pygame.init()

# Window options
window_height = 320
window_width = 240
play_surface = pygame.display.set_mode((window_height,window_width))
pygame.display.set_caption('Snake Game')
# image1 = pygame.image.load(os.path.join('image','image2.jpg'))

# Snakes options
snake_pos = [50,50]
snake_body = [[50,50],[40,50],[30,50]]
direction = 'RIGHT'
changeto = direction

# food options
food_spawn = False
great_food_spawn = False
great_food_pos = [0,0]
apple1_image = pygame.image.load(os.path.join('image','apple1.png'))
apple2_image = pygame.image.load(os.path.join('image','apple2.png'))

# Colors
blue = pygame.Color(0,100,150) # Border
red = pygame.Color(255,0,0) # Gameover
green = pygame.Color(0,255,0) #Snake body
dark_green = pygame.Color(0,150,0) #Snake head
black = pygame.Color(0,0,0) #Score and level
white = pygame.Color(240,255,255) #Background
brown = pygame.Color(165,42,42) #Food

# FPS controller
fps_controller = pygame.time.Clock()

# speed and level options
speed = 4
score = 0
rate = 0
level = 1
RUNNING, PAUSE = 0, 1
state = RUNNING



