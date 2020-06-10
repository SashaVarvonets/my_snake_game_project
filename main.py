import os
import sys
import time
import random
import pygame

DEBUG = int(os.environ.get('DEBUG', '0'))

# ============================================= GAME DRAWING VARIABLES =================================================
# Cell sizes in pixels
cell_size = 20
# Window width and height in pixels
window_w_in_pixels = 800
window_h_in_pixels = 600

#  Multiplicity check
assert window_w_in_pixels % cell_size == 0, "Window width must be a multiple of cell size."
assert window_h_in_pixels % cell_size == 0, "Window height must be a multiple of cell size."
window_w_in_cells = int(window_w_in_pixels / cell_size)
window_h_in_cells = int(window_h_in_pixels / cell_size)

# Colors RGB
red = pygame.Color(255, 0, 0)  # Game over
green = pygame.Color(0, 255, 0)  # Snake body
dark_green = pygame.Color(0, 100, 0)  # Snake head
black = pygame.Color(0, 0, 0)  # Score and level
white = pygame.Color(240, 255, 255)  # Background
brown = pygame.Color(165, 42, 42)  # Food
grey = pygame.Color(40, 40, 40)  # Border

# fonts
pygame.init()
snake_font = pygame.font.Font('freesansbold.ttf', int(window_w_in_pixels / 20))

# =====================================================================================================================
# ============================================ GAME PROCESSING VARIABLE================================================
play_surface = pygame.display.set_mode((window_w_in_pixels, window_h_in_pixels))
fps_controller = pygame.time.Clock()

# Cell coordinate index
X, Y = 0, 1
# =====================================================================================================================


class Game:
    """
    Game could be in 1 of 4 conditions: "WAITING" | "RUNNING" | "PAUSE" | "GAME OVER"
    """
    def __init__(self):
        self.score = 1
        self.level = 0
        self.speed = 3

        self.GAME_CONDITION = "WAITING"

    def draw_screen(self, snake, food, bonus_food):

        if self.GAME_CONDITION == "RUNNING":
            self.draw_background()
            snake.draw()
            food.draw()
            if bonus_food.position != [0, 0]:
                bonus_food.draw()
        elif self.GAME_CONDITION in ("WAITING", "GAME OVER"):
            self.draw_start_menu()
        elif self.GAME_CONDITION == "PAUSE":
            self.draw_pause()
        self.draw_score()
        self.draw_level()
        pygame.display.flip()
        fps_controller.tick(self.speed)

    def draw_start_menu(self):
        pygame.display.set_caption('Snake Game')
        play_surface.fill(black)

        if self.GAME_CONDITION == "WAITING":
            surface = snake_font.render('START GAME!', True, dark_green)
        else:  # GAME_CONDITION == "GAME OVER":
            surface = snake_font.render('Game over!', True, red)

        start_rect = surface.get_rect()
        start_rect.midtop = (window_w_in_pixels / 2, window_h_in_pixels / 5 * 2)
        play_surface.blit(surface, start_rect)

        press_key_surf = snake_font.render('Press SPACE to start', True, white)
        press_key_rect = press_key_surf.get_rect()
        press_key_rect.midtop = (window_w_in_pixels / 2, window_h_in_pixels - window_h_in_pixels / 5)
        play_surface.blit(press_key_surf, press_key_rect)

    def draw_score(self):
        score_surf = snake_font.render('Score: {0}'.format(self.score), True, white)
        score_rect = score_surf.get_rect()
        if self.GAME_CONDITION == "RUNNING":
            score_rect.midtop = (window_w_in_pixels / 9, cell_size)  # Normal position
        else:
            score_rect.midtop = (window_w_in_pixels-(window_w_in_pixels/5), window_h_in_pixels/10)  # Game over position
        play_surface.blit(score_surf, score_rect)

    def draw_level(self):
        score_surf = snake_font.render('Level: {0}'.format(self.level), True, white)
        score_rect = score_surf.get_rect()
        if self.GAME_CONDITION == "RUNNING":
            score_rect.midtop = (window_w_in_pixels - (window_h_in_pixels/7), cell_size)  # Normal position
        else:
            score_rect.midtop = (window_w_in_pixels/5, window_h_in_pixels/10)  # Game over position
        play_surface.blit(score_surf, score_rect)

    def draw_background(self):
        # Background
        play_surface.fill(black)

        # Border
        border = pygame.Rect((0, 0), (window_w_in_pixels, window_h_in_pixels))
        pygame.draw.rect(play_surface, dark_green, border, cell_size)

        # Draw grid lines
        for x in range(int(cell_size / 2), window_w_in_pixels, cell_size):  # draw vertical lines
            pygame.draw.line(play_surface, grey,
                             (x, cell_size / 2),
                             (x, window_h_in_pixels - cell_size / 2))
        for y in range(int(cell_size / 2), window_h_in_pixels, cell_size):  # draw horizontal lines
            pygame.draw.line(play_surface, grey,
                             (cell_size / 2, y),
                             (window_w_in_pixels - cell_size / 2, y))

    def draw_pause(self):
        pause_font = pygame.font.SysFont('freesansbold.ttf', int(window_h_in_pixels/7.5))
        pause_surf = pause_font.render('Pause', True, white)
        pause_rect = pause_surf.get_rect()
        pause_rect.midtop = (window_w_in_pixels/2, window_h_in_pixels/2)
        play_surface.blit(pause_surf, pause_rect)

    # ============================================== GAME MECHANISM ==================================================

    def get_key_press(self):
        pressed_key = None
        for event in pygame.event.get():
            # Quit the game
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif self.GAME_CONDITION == "RUNNING":
                if event.key == ord('p'):  # pause the game
                    self.GAME_CONDITION = "PAUSE"
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        pressed_key = 'RIGHT'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        pressed_key = 'LEFT'
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        pressed_key = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        pressed_key = 'DOWN'

                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.speed += 5
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                        self.speed -= 5
                break
            elif self.GAME_CONDITION == "PAUSE":
                if event.type == pygame.KEYDOWN and event.key == ord('o'):  # run game back from pause
                    self.GAME_CONDITION = "RUNNING"
                    break

            elif self.GAME_CONDITION in ("WAITING", "GAME OVER"):
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    pressed_key = "START"
        return pressed_key

    def update_score(self, points=1):
        self.score += points

        if self.score / 10 >= self.level:
            self.level += 1
            self.speed += 1

    def reset_stat(self):
        self.score = 0
        self.level = 1
        self.speed = 3


class Snake:
    def __init__(self):
        self.head = [
            random.randint(5, window_w_in_cells - cell_size),
            random.randint(5, window_h_in_cells - cell_size)
        ]
        self.body = [[self.head[X] - 1, self.head[Y]], [self.head[X] - 2, self.head[Y]]]
        self.current_direction = "RIGHT"
        self.reached_food = False

    def draw(self):
        # Draw Snake body
        for el in self.body:
            rect_body = pygame.Rect(el[X] * cell_size + cell_size / 2, el[Y] * cell_size + cell_size / 2,
                                    cell_size, cell_size)
            pygame.draw.rect(play_surface, dark_green, rect_body, 2)

        # Draw head
        rect_head = pygame.Rect(self.head[X] * cell_size + cell_size / 2 + 2,
                                self.head[Y] * cell_size + cell_size / 2 + 2, cell_size - 3, cell_size - 3)
        pygame.draw.rect(play_surface, green, rect_head)

    def change_direction(self, new_direction):
        if new_direction == 'RIGHT' and self.current_direction != 'LEFT':
            self.current_direction = 'RIGHT'
        elif new_direction == 'LEFT' and self.current_direction != 'RIGHT':
            self.current_direction = 'LEFT'
        elif new_direction == 'UP' and self.current_direction != 'DOWN':
            self.current_direction = 'UP'
        elif new_direction == 'DOWN' and self.current_direction != 'UP':
            self.current_direction = 'DOWN'

    def make_step(self):
        self.body.insert(0, self.head.copy())

        if self.current_direction == 'RIGHT':
            self.head[X] += 1
        elif self.current_direction == 'LEFT':
            self.head[X] -= 1
        elif self.current_direction == 'UP':
            self.head[Y] -= 1
        elif self.current_direction == 'DOWN':
            self.head[Y] += 1

        if self.head in self.body:
            raise  # Collision with body

        # if not (left_border < head-X < right_border) or not (ceiling_border < head-Y < bottom_border)
        if not (-1 < self.head[X] < window_w_in_cells - 1) or not (-1 < self.head[Y] < window_h_in_cells - 1):
            raise  # Collision with border

        # If food has been reached, then the body of the snake lengthens (the last element is not removed)
        if self.reached_food:
            self.reached_food = False
        else:
            self.body.pop()


class Food:
    apple_images = {
        10: 'pictures/red10.png',
        20: 'pictures/red20.png',
        40: 'pictures/red40.png',
    }

    def __init__(self):
        self.picture = self.apple_images.get(cell_size, None)
        self.default_color = red
        self.position = []

    def draw(self):
        # Draw food
        if self.picture:
            loaded_picture = pygame.image.load(self.picture)
            play_surface.blit(loaded_picture, (self.position[X] * cell_size + cell_size / 2,
                                               self.position[Y] * cell_size + cell_size / 2))
        else:
            rect_apple = pygame.Rect(self.position[X] * cell_size + cell_size / 2 + 1,
                                     self.position[Y] * cell_size + cell_size / 2 + 1,
                                     cell_size - 1, cell_size - 1)
            pygame.draw.rect(play_surface, self.default_color, rect_apple)

    def find_new_place(self, snake):
        new_place = [random.randrange(1, window_w_in_cells - 1), random.randrange(3, window_h_in_cells - 1)]
        if new_place in snake.body or new_place == snake.head:
            self.find_new_place(snake)
        else:
            self.position = new_place


class BonusFood(Food):
    bonus_apple_images = {
        10: 'pictures/white10.png',
        20: 'pictures/white20.png',
        40: 'pictures/white40.png',
    }

    def __init__(self):
        super().__init__()
        self.picture = self.bonus_apple_images.get(cell_size, None)
        self.default_color = white
        self.position = [0, 0]
        self.timer = None

    def start_timer(self):
        self.timer = time.time()

    def check_timer(self):
        now = time.time()
        if now - self.timer > 5:  # Hide bonus food
            self.position = [0, 0]
            self.timer = None


def start_game():
    snake = Snake()
    game = Game()
    food = Food()
    bonus_food = BonusFood()

    RUN = True
    while RUN:
        key_press = game.get_key_press()
        if game.GAME_CONDITION == "RUNNING":
            if key_press:
                snake.change_direction(key_press)

            try:
                snake.make_step()
            except:
                game.GAME_CONDITION = 'GAME OVER'

            if snake.head == food.position:
                # adding bonus only if food was eaten and only when update a score (to avoid reappearance bonus food)
                if bonus_food.position == [0, 0] and game.score > 7 and game.score % 8 == 0:
                    bonus_food.find_new_place(snake)
                    bonus_food.start_timer()

                game.update_score()
                food.find_new_place(snake)
                snake.reached_food = True

            if snake.head == bonus_food.position:
                game.update_score(5)
                bonus_food.position = [0, 0]
            elif bonus_food.position != [0, 0]:
                bonus_food.check_timer()

        elif game.GAME_CONDITION in ("WAITING", "GAME OVER"):
            if key_press:
                game.reset_stat()
                snake = Snake()
                food.find_new_place(snake)
                game.GAME_CONDITION = 'RUNNING'

        game.draw_screen(snake, food, bonus_food)


if __name__ == '__main__':
    # TODO:
    #  - find a way to clear event loop after getting key_press
    #  - find a way to separate FPS and game_speed
    #  - add option to play with|without border
    #  - save score in DB with name
    #  - see top 10 cores with names
    #  - add option to choose cell size
    #  - add sound and music

    start_game()
