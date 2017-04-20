import pygame, sys, random, time, os
from pygame.locals import * 
pygame.init()


# Important variables
window_height = 200
window_width = 100
snake_pos = [50,50]
snake_body = [[50,50],[40,50],[30,50]]

# Colors
blue = pygame.Color(0,100,150) # Border
red = pygame.Color(255,0,0) # Gameover
green = pygame.Color(0,255,0) #Snake body
dark_green = pygame.Color(0,150,0) #Snake head
black = pygame.Color(0,0,0) #Score and level
white = pygame.Color(240,255,255) #Background
brown = pygame.Color(165,42,42) #Food

food_spawn = False

direction = 'RIGHT'
changeto = direction

speed = 4
score = 0
level = 1

RUNNING, PAUSE = 0, 1
state = RUNNING





# Play surface
play_surface = pygame.display.set_mode((window_height,window_width))
pygame.display.set_caption('Snake Game')

# image1 = pygame.image.load(os.path.join('image','image2.jpg'))
# newSurf = pygame.Surface((window_width-20, window_height-40))
# newSurf.blit(image1, (0,0))

# FPS controller
fps_controller = pygame.time.Clock()