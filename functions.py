import pygame
import sys
import random

from drow_functions import window_width_size, window_height_size

# Import funcs to draw start menu
from drow_functions import draw_menu, draw_score, draw_level
# Import funcs to draw game process
from drow_functions import draw_background, draw_snake, draw_food, draw_great_food, draw_pause


pygame.init()

# Speed and level options
speed = 3
score = 0
rate = 0
level = 1

# Food options
food_spawn = False
great_food_spawn = False
game_status = True

fps_controller = pygame.time.Clock()


def show_menu_screen():
    while True:
        draw_menu(game_status)
        draw_score(score, choice=False)
        draw_level(level, choice=False)
        if check_for_key_press():
            return
        pygame.display.flip()
        fps_controller.tick(speed)


def check_for_key_press():
    events = pygame.event.get()
    if not events:
        return
    if events[0].type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif events[0].type == pygame.KEYDOWN:
        if events[0].key != pygame.K_ESCAPE:
            return True
        else:
            pygame.quit()
            sys.exit()


def run_game():
    global speed, rate, level, score, game_status

    global food_pos, food_spawn, great_food_pos, great_food_spawn

    running_game = True

    start_x = random.randint(5, window_width_size - 10)
    start_y = random.randint(5, window_height_size - 6)
    snake_pos = [start_x, start_y]
    snake_body = [[start_x, start_y], [start_x - 1, start_y], [start_x - 2, start_y]]
    direction = 'RIGHT'
    changeto = direction
    # Main Logic of the game
    while True:
        # Increase speed
        if rate >= speed * level * 2:
            speed += 1
            level += 1

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('p'):
                    running_game = True
                if event.key == ord('o'):
                    running_game = False
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
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    speed -= 5

        # Game scene
        if running_game:
            # Validation of direction
            if changeto == 'RIGHT' and not direction == 'LEFT':
                direction = 'RIGHT'
            elif changeto == 'LEFT' and not direction == 'RIGHT':
                direction = 'LEFT'
            elif changeto == 'UP' and not direction == 'DOWN':
                direction = 'UP'
            elif changeto == 'DOWN' and not direction == 'UP':
                direction = 'DOWN'

            # Update snake position[x,y]
            if direction == 'RIGHT':
                snake_pos[0] += 1
            elif direction == 'LEFT':
                snake_pos[0] -= 1
            elif direction == 'UP':
                snake_pos[1] -= 1
            elif direction == 'DOWN':
                snake_pos[1] += 1

            # Gt Food
            if not food_spawn:
                food_pos = get_food(snake_body)
                food_spawn = True

            # Get Great food and start timing
            if rate % 8 == 0:
                great_food_spawn = True
                great_food_pos = get_food(snake_body)
                global timing_value
                timing_value = start_timing()
                rate += 1

            # Check for stop timing
            if great_food_spawn:
                stop_timing()

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

            # Collision with border
            if snake_pos[0] > window_width_size - 2 or snake_pos[0] < 0:
                game_status = False
                return  # game_over
            if snake_pos[1] > window_height_size - 2 or snake_pos[1] < 0:
                game_status = False
                return  # game_over

            # Collision with body
            for block in snake_body[1:]:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    game_status = False
                    return  # game_over

        else:
            # Pause scene
            draw_pause()
        draw_background()
        draw_snake(snake_body, snake_pos)
        draw_food(food_pos)
        if great_food_spawn:
            draw_great_food(great_food_pos)

        draw_score(score)
        draw_level(level)

        pygame.display.flip()
        fps_controller.tick(speed)


def get_food(snake_body):
    get_pos = [random.randrange(1, window_width_size-1), random.randrange(3, window_height_size-1)]

    if get_pos in snake_body:
        return get_food(snake_body)
    else:
        return get_pos


# Start timing func for great food
def start_timing():
    return pygame.time.get_ticks()


# Stop timing func for great food
def stop_timing():
    global great_food_pos, great_food_spawn
    now = pygame.time.get_ticks()
    cool_dawn = 5000
    if now - timing_value >= cool_dawn:
        great_food_pos = [0, 0]
        great_food_spawn = False
