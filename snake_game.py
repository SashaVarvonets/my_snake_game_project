# Snake Game!

# Imports for game
import pygame, sys, random, time, os
from pygame.locals import * 
from variables import *

# Game over function
def game_over():
    my_font = pygame.font.SysFont('monaco', int(window_height//10))
    game_over_surf = my_font.render('Game over!',True, red)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (window_height/2,window_width/4)
    play_surface.blit(game_over_surf,game_over_rect)
    show_score(0)
    show_level(0)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Score function
def show_score(choice=1):
    score_font = pygame.font.SysFont('monaco', window_height//25)
    score_surf = score_font.render('Score: {0}'.format(score),True, black)
    score_rect = score_surf.get_rect()
    if choice == 1:
        score_rect.midtop = (window_height/10,5)
    else:
        score_rect.midtop = (window_height//2,window_width//2.3)
    play_surface.blit(score_surf,score_rect)


def show_level(choice=1):
    score_font = pygame.font.SysFont('monaco', int(window_height//25))
    score_surf = score_font.render('Level: {0}'.format(level),True, black)
    score_rect = score_surf.get_rect()
    if choice == 1:
        score_rect.midtop = (window_height-(window_height/10),5)
    else:
        score_rect.midtop = (window_height//2,window_width//2)
    play_surface.blit(score_surf,score_rect)

# Getting food function
def get_food():
    get_pos = [random.randrange(1,(window_height-10)/10)*10,\
               random.randrange(3,(window_width-10)/10)*10]
    if get_pos in list(snake_body):
        return get_food()
    else:
        return get_pos

def pause_func():
    pause_font = pygame.font.SysFont('monaco', int(window_height/7.5))
    pause_surf = pause_font.render('Pause', True, black)
    pause_rect = pause_surf.get_rect()
    pause_rect.midtop = (window_height/2,window_width/2)
    play_surface.blit(pause_surf,pause_rect)

def draw_func():
    #border
    border = Rect((3,23),(window_height-8,window_width-28))
    pygame.draw.rect(play_surface,blue,border, 10) 
    # play_surface.blit(newSurf, (10,30))

    # Draw Snake
    for pos in snake_body:
        pygame.draw.rect(play_surface, green,
        pygame.Rect(pos[0]-1,pos[1]-1,11,11),2)

    # Draw head
    pygame.draw.rect(play_surface, dark_green,
    pygame.Rect(snake_pos[0],snake_pos[1],10,10))

    # Draw Food
    pygame.draw.rect(play_surface, brown,
    pygame.Rect(food_pos[0],food_pos[1],10,10))

# Pygame initializing
pygame.init()

# Main Logic of the game
while True:
    # Increase speed
    if score  >= speed*level:
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
                speed +=5
            if event.key == pygame.K_LCTRL:
                pygame.time.delay(1)
        elif event.type == KEYUP:
            if event.key == pygame.K_SPACE:
                speed -=5

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
            snake_pos[0] +=10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
    
        # Food spawn
        if food_spawn == False:
            food_pos = get_food()
        food_spawn = True
    
        # Snake body mechanism
        snake_body.insert(0,list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()
    
        # Background
        play_surface.fill(white)
        draw_func()
        # Bound
        if snake_pos[0] > window_height-20 or snake_pos[0] < 10:
            game_over()
        if snake_pos[1] > window_width-20 or snake_pos[1] < 25:
            game_over()
    
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        show_score()
        show_level()
        pygame.display.flip()
        fps_controller.tick(speed)

    elif state == PAUSE:
        play_surface.fill(white)
        time.sleep(0.5)
        draw_func()
        pause_func()
        show_score()
        show_level()
        pygame.display.flip()
        fps_controller.tick(speed)

