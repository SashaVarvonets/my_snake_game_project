# Snake Game!

# Imports for game
import sys
import random
import time
import pygame

from pygame.locals import * 
from variables import *

def main():
    global fps_controller, play_surface, snake_font

    pygame.init()
    fps_controller = pygame.time.Clock()
    play_surface = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('Snake Game')
    snake_font = pygame.font.Font('freesansbold.ttf', int(window_height/18))

    show_start_screen()
    while True:
        run_game()
        game_over()

def run_game():
    global rate,speed,score,level, state,food_spawn,\
           snake_body, snake_pos, great_food_pos,\
           great_food_spawn, food_pos 

    speed = 4
    score = 0
    rate = 0
    level = 1
    great_food_pos = [0, 0]
    great_food_spawn = False

    start_x = random.randint(5, window_width_size - 10)
    start_y = random.randint(5, window_height_size - 6)
    snake_pos = [start_x, start_y]
    snake_body = [[start_x, start_y], [start_x-1, start_y], [start_x-2, start_y]]
    direction = 'RIGHT'
    changeto = direction
    # Main Logic of the game
    while True:
        # Increase speed
        if rate  >= speed*level*2:
            speed += 1
            level += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('p'):
                    state = PAUSE
                if event.key == ord('o'):
                    state = RUNNING
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeto = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeto = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    changeto = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    changeto = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_SPACE:
                    speed += 5
            elif event.type == KEYUP:
                if event.key == pygame.K_SPACE:
                    speed -= 5
        # Game scene
        if state == RUNNING:
            # Validation of direction
            if changeto == 'RIGHT' and not direction == 'LEFT':
                direction = 'RIGHT'
            if changeto == 'LEFT' and not direction == 'RIGHT':
                direction = 'LEFT'
            if changeto == 'UP' and not direction == 'DOWN':
                direction = 'UP'
            if changeto == 'DOWN' and not direction == 'UP':
                direction = 'DOWN'
        
            # Update snake position[x,y]
            if direction == 'RIGHT':
                snake_pos[0] += 1
            if direction == 'LEFT':
                snake_pos[0] -= 1
            if direction == 'UP':
                snake_pos[1] -= 1
            if direction == 'DOWN':
                snake_pos[1] += 1
        
            # Gt Food
            if food_spawn == False:
                food_pos = get_food()
                food_spawn = True
            
            # Get Great food and start timing
            if rate > 0 and rate%8 == 0:
                great_food_spawn = True
                great_food_pos = get_food()
                start_time()
                rate += 1

            # Check for stop timing
            if great_food_spawn == True:
                stop_time()

            # Eating great food
            if snake_pos[0] == great_food_pos[0] and snake_pos[1] == great_food_pos[1]:
                score += 10
                great_food_spawn = False
                great_food_pos = [0, 0]
        
            # Snake body mechanism
            snake_body.insert(0, list(snake_pos))
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                score += 1
                rate += 1
                food_spawn = False
            else:
                snake_body.pop()
        
            # Background
            play_surface.fill(black)

            if great_food_spawn == True:
                draw_func(0)
            else:
                draw_func()

            # Сollision with border
            if snake_pos[0] > window_width_size-2 or snake_pos[0] < 0:
                return #game_over
            if snake_pos[1] > window_height_size-2 or snake_pos[1] < 0:
                return # game_over
            
            # Сollision with body
            for block in snake_body[1:]:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    return # game_over

            show_score()
            show_level()
            pygame.display.flip()
            fps_controller.tick(speed)
        # Pause scene
        elif state == PAUSE:
            play_surface.fill(black)
            if great_food_spawn == True:
                draw_func(0)
            else:
                draw_func()
            pause_func()
            show_score()
            show_level()
            pygame.display.flip()
            fps_controller.tick(speed)

# Start timing func for great food
def start_time():
    global last
    last = pygame.time.get_ticks()

# Stop timing func for great food
def stop_time():
    global now, great_food_spawn, great_food_pos
    now = pygame.time.get_ticks()
    cooldawn = 5000
    if now - last >= cooldawn:
        great_food_spawn = False
        great_food_pos = [0,0]

# Start scene
def show_start_screen():
    while True:
        play_surface.fill(black)
        start_font = pygame.font.SysFont('freesansbold.ttf', 100)
        start_surf = start_font.render('START', True, dark_green)
        start_rect = start_surf.get_rect()
        start_rect.midtop = (window_width/2, window_height/5*2)
        play_surface.blit(start_surf, start_rect)
        draw_start()
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.flip()
        fps_controller.tick(speed)


def draw_start():
    #Press key str
    pressKeySurf = snake_font.render('Press any key to start', True, white)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.midtop = (window_width/2, window_height - window_height/5)
    play_surface.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        pygame.quit()
        sys.exit()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return
    if keyUpEvents[0].key == K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyUpEvents[0].key

# Score function
def show_score(choice=1):
    score_surf = snake_font.render('Score: {0}'.format(score), True, white)
    score_rect = score_surf.get_rect()
    if choice == 1:
        score_rect.midtop = (window_width/9, snake_size)# Normal position
    else:
        score_rect.midtop = (window_width//5*3, window_height//4*1) # Game over position
    play_surface.blit(score_surf, score_rect)

# Level function
def show_level(choice=1):
    score_surf = snake_font.render('Level: {0}'.format(level), True, white)
    score_rect = score_surf.get_rect()
    if choice == 1:
        score_rect.midtop = (window_width-(window_width/9), snake_size) # Normal position
    else:
        score_rect.midtop = (window_width/5*2, window_height/4*1) # Game over position
    play_surface.blit(score_surf, score_rect)

# Getting food function
def get_food():
    get_pos = [random.randrange(1, window_width_size-1),\
               random.randrange(3, window_height_size-1)]
    if get_pos in list(snake_body):
        return get_food()
    else:
        return get_pos

def pause_func():
    pause_font = pygame.font.SysFont('freesansbold.ttf',
                                     int(window_height/7.5))
    pause_surf = pause_font.render('Pause', True, white)
    pause_rect = pause_surf.get_rect()
    pause_rect.midtop = (window_width/2, window_height/2)
    play_surface.blit(pause_surf, pause_rect)

def draw_func(choice=1):
    #border
    border = Rect((0,0),(window_width, window_height))
    pygame.draw.rect(play_surface, dark_green, border, snake_size)


    # Draw grid lines
    for x in range(int(snake_size/2), window_width, snake_size): # draw vertical lines
        pygame.draw.line(play_surface, grey,
                        (x, snake_size/2),
                        (x, window_height-snake_size/2))
    for y in range(int(snake_size/2),window_height, snake_size): # draw horizontal lines
        pygame.draw.line(play_surface, grey,
                        (snake_size/2, y),
                        (window_width-snake_size/2, y))

    # Draw Snake body
    for pos in snake_body:
        pygame.draw.rect(play_surface, green,
        pygame.Rect(pos[0]*snake_size+snake_size/2,
                    pos[1]*snake_size+snake_size/2,
                    snake_size,snake_size),2)

    # Draw head
    pygame.draw.rect(play_surface, dark_green,
    pygame.Rect(snake_pos[0]*snake_size+snake_size/2+2,
                snake_pos[1]*snake_size+snake_size/2+2,
                snake_size-3,snake_size-3))

    # Draw food
    if snake_size == 10:
        # Normal apple
        play_surface.blit(apple_red_10,
                         (food_pos[0]*snake_size+snake_size/2,
                          food_pos[1]*snake_size+snake_size/2))
        if choice!=1: # Great apple
            play_surface.blit(apple_white_10,
                             (great_food_pos[0]*snake_size+snake_size/2,\
                              great_food_pos[1]*snake_size+snake_size/2))
    elif snake_size == 20:
        # Normal apple
        play_surface.blit(apple_red_20,
                         (food_pos[0]*snake_size+snake_size/2,
                          food_pos[1]*snake_size+snake_size/2))
        if choice!=1: # Great apple
            play_surface.blit(apple_white_20,
                             (great_food_pos[0]*snake_size+snake_size/2,\
                              great_food_pos[1]*snake_size+snake_size/2))
    elif snake_size == 40:
        # Normal apple
        play_surface.blit(apple_red_40,
                         (food_pos[0]*snake_size+snake_size/2,
                          food_pos[1]*snake_size+snake_size/2))
        if choice!=1: # Great apple
            play_surface.blit(apple_white_40,
                             (great_food_pos[0]*snake_size+snake_size/2,\
                              great_food_pos[1]*snake_size+snake_size/2))
    else:
        # Normal apple
        pygame.draw.rect(play_surface, red,
        pygame.Rect(food_pos[0]*snake_size+snake_size/2+1,
                    food_pos[1]*snake_size+snake_size/2+1,
                    snake_size-1,snake_size-1))
        if choice!=1 :# Great apple
            pygame.draw.rect(play_surface, white,
            pygame.Rect(great_food_pos[0]*snake_size+snake_size/2+1,
                        great_food_pos[1]*snake_size+snake_size/2+1,
                        snake_size-1,snake_size-1))


# Game over function
def game_over():
    game_over_font = pygame.font.SysFont('freesansbold.ttf', 100)
    game_over_surf = game_over_font.render('Game over!', True, red)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (window_width/2, window_height/5*2)
    play_surface.blit(game_over_surf, game_over_rect)
    show_score(0)
    show_level(0)
    draw_start()
    pygame.display.flip()
    checkForKeyPress() # clear out any key presses in the event queue
    while True:

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()