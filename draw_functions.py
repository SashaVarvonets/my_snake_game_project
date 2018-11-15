import pygame

pygame.init()

# Window options in px
window_width = 800
window_height = 600
cell_size = 20

#  Multiplicity check
assert window_width % cell_size == 0, "Window width must be a multiple of cell size."
assert window_height % cell_size == 0, "Window height must be a multiple of cell size."


window_width_size = int(window_width / cell_size)
window_height_size = int(window_height / cell_size)
play_surface = pygame.display.set_mode((window_width, window_height))
fps_controller = pygame.time.Clock()

# fonts
snake_font = pygame.font.Font('freesansbold.ttf', int(window_height / 20))

# apple images
apple_red_10 = pygame.image.load('pictures/red10.png')
apple_white_10 = pygame.image.load('pictures/white10.png')
apple_red_20 = pygame.image.load('pictures/red20.png')
apple_white_20 = pygame.image.load('pictures/white20.png')
apple_red_40 = pygame.image.load('pictures/red40.png')
apple_white_40 = pygame.image.load('pictures/white40.png')

# Colors RGB
red = pygame.Color(255, 0, 0)  # Game over
green = pygame.Color(0, 255, 0)  # Snake body
dark_green = pygame.Color(0, 100, 0)  # Snake head
black = pygame.Color(0, 0, 0)  # Score and level
white = pygame.Color(240, 255, 255)  # Background
brown = pygame.Color(165, 42, 42)  # Food
grey = pygame.Color(40, 40, 40)  # Border


def draw_menu(game_status):
    pygame.display.set_caption('Snake Game')
    play_surface.fill(black)
    if game_status:
        surface = snake_font.render('START GAME!', True, dark_green)
    else:
        surface = snake_font.render('Game over!', True, red)
    start_rect = surface.get_rect()
    start_rect.midtop = (window_width / 2, window_height / 5 * 2)
    play_surface.blit(surface, start_rect)

    press_key_surf = snake_font.render('Press SPACE to start', True, white)
    press_key_rect = press_key_surf.get_rect()
    press_key_rect.midtop = (window_width / 2, window_height - window_height / 5)
    play_surface.blit(press_key_surf, press_key_rect)


def draw_score(score, choice=True):
    score_surf = snake_font.render('Score: {0}'.format(score), True, white)
    score_rect = score_surf.get_rect()
    if choice:
        score_rect.midtop = (window_width / 9, cell_size)  # Normal position
    else:
        score_rect.midtop = (window_width-(window_width/5), window_height/10)  # Game over position
    play_surface.blit(score_surf, score_rect)


def draw_level(level, choice=True):
    score_surf = snake_font.render('Level: {0}'.format(level), True, white)
    score_rect = score_surf.get_rect()
    if choice:
        score_rect.midtop = (window_width - (window_height/9), cell_size)  # Normal position
    else:
        score_rect.midtop = (window_width/5, window_height/10)  # Game over position
    play_surface.blit(score_surf, score_rect)


def draw_background():
    # Background
    play_surface.fill(black)

    # Border
    border = pygame.Rect((0, 0), (window_width, window_height))
    pygame.draw.rect(play_surface, dark_green, border, cell_size)

    # Draw grid lines
    for x in range(int(cell_size / 2), window_width, cell_size):  # draw vertical lines
        pygame.draw.line(play_surface, grey,
                         (x, cell_size / 2),
                         (x, window_height - cell_size / 2))
    for y in range(int(cell_size / 2), window_height, cell_size):  # draw horizontal lines
        pygame.draw.line(play_surface, grey,
                         (cell_size / 2, y),
                         (window_width - cell_size / 2, y))


def draw_snake(snake_body, snake_pos):
    # Draw Snake body
    for pos in snake_body:
        rect_body = pygame.Rect(pos[0] * cell_size + cell_size / 2, pos[1] * cell_size + cell_size / 2, cell_size, cell_size)
        pygame.draw.rect(play_surface, green, rect_body, 2)

    # Draw head
    rect_head = pygame.Rect(snake_pos[0] * cell_size + cell_size / 2 + 2,
                            snake_pos[1] * cell_size + cell_size / 2 + 2, cell_size - 3, cell_size - 3)
    pygame.draw.rect(play_surface, dark_green, rect_head)


def draw_food(food_pos):
    # Draw food
    if cell_size == 10:
        play_surface.blit(apple_red_10, (food_pos[0] * cell_size + cell_size / 2, food_pos[1] * cell_size + cell_size / 2))
    elif cell_size == 20:
        play_surface.blit(apple_red_20, (food_pos[0] * cell_size + cell_size / 2, food_pos[1] * cell_size + cell_size / 2))
    elif cell_size == 40:
        play_surface.blit(apple_red_40, (food_pos[0] * cell_size + cell_size / 2, food_pos[1] * cell_size + cell_size / 2))
    else:
        rect_apple = pygame.Rect(food_pos[0] * cell_size + cell_size / 2 + 1,
                                 food_pos[1] * cell_size + cell_size / 2 + 1, cell_size - 1, cell_size - 1)
        pygame.draw.rect(play_surface, red, rect_apple)


def draw_great_food(great_food_pos):
    if cell_size == 10:
        play_surface.blit(apple_white_10, (great_food_pos[0] * cell_size + cell_size / 2,
                                           great_food_pos[1] * cell_size + cell_size / 2))
    elif cell_size == 20:
        play_surface.blit(apple_white_20, (great_food_pos[0] * cell_size + cell_size / 2,
                                           great_food_pos[1] * cell_size + cell_size / 2))
    elif cell_size == 40:
        play_surface.blit(apple_white_40, (great_food_pos[0] * cell_size + cell_size / 2,
                                           great_food_pos[1] * cell_size + cell_size / 2))
    else:
        rect_apple = pygame.Rect(great_food_pos[0] * cell_size + cell_size / 2 + 1,
                                 great_food_pos[1] * cell_size + cell_size / 2 + 1, cell_size - 1, cell_size - 1)
        pygame.draw.rect(play_surface, white, rect_apple)


def draw_pause():
    pause_font = pygame.font.SysFont('freesansbold.ttf', int(window_height/7.5))
    pause_surf = pause_font.render('Pause', True, white)
    pause_rect = pause_surf.get_rect()
    pause_rect.midtop = (window_width/2, window_height/2)
    play_surface.blit(pause_surf, pause_rect)
