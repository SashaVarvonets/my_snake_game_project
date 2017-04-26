import pygame

pygame.init()

# Window options
window_width = 800
window_height = 600
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
# apple images
apple_red_10 = pygame.image.load('red10.png')
apple_white_10 = pygame.image.load('white10.png')
apple_red_20 = pygame.image.load('red20.png')
apple_white_20 = pygame.image.load('white20.png')
apple_red_40 = pygame.image.load('red40.png')
apple_white_40 = pygame.image.load('white40.png')

# Colors RGB
red = pygame.Color(255,0,0) # Gameover
green = pygame.Color(0,255,0) #Snake body
dark_green = pygame.Color(0,100,0) #Snake head
black = pygame.Color(0,0,0) #Score and level
white = pygame.Color(240,255,255) #Background
brown = pygame.Color(165,42,42) #Food
grey = pygame.Color(40,40,40) # Border

# Speed and level options
speed = 3
score = 0
rate = 0
level = 1
RUNNING, PAUSE = 0, 1
state = RUNNING