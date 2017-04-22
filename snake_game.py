# Snake Game!

# Imports for game
import pygame, sys, random, time, os
from pygame.locals import * 
from variables import *

def main():
    global fps_controller, play_surface

    pygame.init()
    fps_controller = pygame.time.Clock()
    play_surface = pygame.display.set_mode((window_height,window_width))
    pygame.display.set_caption('Snake Game')

    showStartScreen()
    while True:
        run_game()
        game_over()

def run_game():
    global rate,speed,score,level, state,food_spawn,snake_body, snake_pos, \
           great_food_pos,great_food_spawn, food_pos 

    speed = 5
    score = 0
    rate = 0
    level = 1
    great_food_pos = [0,0]
    great_food_spawn = False


    snake_pos = [50,50]
    snake_body = [[50,50],[40,50],[30,50]]
    direction = 'RIGHT'
    changeto = direction
    # Main Logic of the game
    while True:
        # Increase speed
        if rate  >= speed*level:
            speed += 1
            level += 1
            print(speed)

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
    
            if rate > 0 and rate%5==0:
                great_food_spawn = True
                great_food_pos = get_food()
                rate += 1

    
            if snake_pos[0] == great_food_pos[0] and snake_pos[1] == great_food_pos[1]:
                score += 10
                great_food_spawn = False
                great_food_pos = [0,0]
        
            # Snake body mechanism
            snake_body.insert(0,list(snake_pos))
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                score += 1
                rate += 1
                food_spawn = False
            else:
                snake_body.pop()
        
            # Background
            play_surface.fill(white)
            if great_food_spawn == True:
                draw_func(0)
            else:
                draw_func()
            # Bound
            if snake_pos[0] > window_height-20 or snake_pos[0] < 10:
                return #game_over
            if snake_pos[1] > window_width-20 or snake_pos[1] < 25:
                return #game_over
        
            for block in snake_body[1:]:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    return #game_over
    
            show_score()
            show_level()
            pygame.display.flip()
            fps_controller.tick(speed)
    
        elif state == PAUSE:
            play_surface.fill(white)
            if great_food_spawn == True:
                draw_func(0)
            else:
                draw_func()
            pause_func()
            show_score()
            show_level()
            pygame.display.flip()
            fps_controller.tick(speed)

def showStartScreen():
    while True:
        play_surface.fill(white)
        drawPressKeyMsg()
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.flip()
        fps_controller.tick(speed)

def drawPressKeyMsg():
    press_font = pygame.font.SysFont('monaco',int(window_height/20))
    pressKeySurf = press_font.render('Press any key to start', True, black)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.midtop = (window_height/2,window_width - window_width/5)
    play_surface.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        pygame.quit()
        sys.exit()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        pygame.quit()
        sys.exit()
    return keyUpEvents[0].key


# Score function
def show_score(choice=1):
    score_font = pygame.font.SysFont('monaco', window_height//25)
    score_surf = score_font.render('Score: {0}'.format(score),True, black)
    score_rect = score_surf.get_rect()
    if choice == 1:
        score_rect.midtop = (window_height/10,5)
    else:
        score_rect.midtop = (window_height//5*2,window_width//4*1)
    play_surface.blit(score_surf,score_rect)

 
def show_level(choice=1):
    score_font = pygame.font.SysFont('monaco', int(window_height//25))
    score_surf = score_font.render('Level: {0}'.format(level),True, black)
    score_rect = score_surf.get_rect()
    if choice == 1:
        score_rect.midtop = (window_height-(window_height/10),5)
    else:
        score_rect.midtop = (window_height//5*3,window_width//4*1)
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

def draw_func(choice=1):
    # play_surface.blit(image1, (0,25))

    #border
    border = Rect((3,23),(window_height-8,window_width-28))
    pygame.draw.rect(play_surface,blue,border, 10) 

    # Draw Snake
    for pos in snake_body:
        pygame.draw.rect(play_surface, green,
        pygame.Rect(pos[0]-1,pos[1]-1,11,11),2)

    # Draw head
    pygame.draw.rect(play_surface, dark_green,
    pygame.Rect(snake_pos[0],snake_pos[1],10,10))

    play_surface.blit(apple1_image,(food_pos[0],food_pos[1]))
    if choice!=1:
        play_surface.blit(apple2_image,(great_food_pos[0],great_food_pos[1]))

# Game over function
def game_over():
    game_over_font = pygame.font.SysFont('monaco',100)
    game_over_surf = game_over_font.render('Game over!',True, red)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (window_height/2,window_width/5*2)
    play_surface.blit(game_over_surf,game_over_rect)
    show_score(0)
    show_level(0)
    drawPressKeyMsg()
    pygame.display.flip()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
    sys.exit()

if __name__ == '__main__':
    main()

