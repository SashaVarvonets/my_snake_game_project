import os
import random
import pygame

from functions import show_menu_screen, run_game

DEBUG = int(os.environ.get('DEBUG', '0'))

# ============================================= GAME DRAW VARIABLE==================================================
# Cell sizes in pixels
cell_size = 10
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
snake_font = pygame.font.Font('freesansbold.ttf', int(window_h_in_cells / 20))

# =====================================================================================================================
# ============================================= GAME PROCESS VARIABLE==================================================
pygame.init()
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
        self.score = 0
        self.level = 0
        self.speed = 0

        self.GAME_CONDITION = "WAITING"

    def draw_screen(self, snake):

        if self.GAME_CONDITION == "RUNNING":
            self.draw_background()
            snake.draw()
            # food.draw()
        elif self.GAME_CONDITION in ("WAITING", "GAME OVER"):
            self.draw_menu()
        elif self.GAME_CONDITION == "PAUSE":
            self.draw_pause()
        self.draw_score()
        self.draw_level()
        pygame.display.flip()
        fps_controller.tick(self.speed)

    def draw_menu(self):
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
            score_rect.midtop = (window_w_in_pixels - (window_h_in_pixels/9), cell_size)  # Normal position
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

    def check_button_click(self):
        new_direction = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == ord('p'):
                    self.GAME_CONDITION = "PAUSE"
                if event.key == ord('o'):
                    self.GAME_CONDITION = "RUNNING"
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    new_direction = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    new_direction = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    new_direction = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    new_direction = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    self.speed += 5
                break
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    self.speed -= 5
                break
        return new_direction


class Snake:
    def __init__(self):
        self.head = [
            random.randint(cell_size, window_w_in_cells - cell_size),
            random.randint(cell_size, window_h_in_cells - cell_size)
        ]
        self.body = [[self.head[X] - 1, self.head[Y]], [self.head[X] - 2, self.head[Y]]]
        self.current_direction = "RIGHT"

    def draw(self):
        # Draw Snake body
        for el in self.body:
            rect_body = pygame.Rect(el[X] * cell_size + cell_size / 2, el[Y] * cell_size + cell_size / 2,
                                    cell_size, cell_size)
            pygame.draw.rect(play_surface, green, rect_body, 2)

        # Draw head
        rect_head = pygame.Rect(self.head[X] * cell_size + cell_size / 2 + 2,
                                self.head[Y] * cell_size + cell_size / 2 + 2, cell_size - 3, cell_size - 3)
        pygame.draw.rect(play_surface, dark_green, rect_head)

    def change_direction(self, new_direction):
        if new_direction == 'RIGHT' and self.current_direction != 'LEFT':
            self.current_direction = 'RIGHT'
        elif new_direction == 'LEFT' and self.current_direction != 'RIGHT':
            self.current_direction = 'LEFT'
        elif new_direction == 'UP' and self.current_direction != 'DOWN':
            self.current_direction = 'UP'
        elif new_direction == 'DOWN' and self.current_direction != 'UP':
            self.current_direction = 'DOWN'

    def make_step(self, food, bonus_food=None):

        self.body.insert(0, self.head)

        if self.current_direction == 'RIGHT':
            self.head[X] += 1
        elif self.current_direction == 'LEFT':
            self.head[X] -= 1
        elif self.current_direction == 'UP':
            self.head[Y] -= 1
        elif self.current_direction == 'DOWN':
            self.head[Y] += 1

        if food.position == self.head:
            food.change_position()
        else:
            self.body.pop()

        if bonus_food and bonus_food.position == self.head:
            bonus_food.change_position()


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
        self.position = []


def start_test_game():
    snake = Snake()
    game = Game()

    RUN = True
    while RUN:
        if game.GAME_CONDITION == "RUNNING":
            pass
            """
            change snake position
            check for collision with border or snake body
            draw snake
            """
        elif game.GAME_CONDITION in ("WAITING", "GAME OVER"):
            pass
            """
            waiting for pressing the start button
            change game status
            """
        elif game.GAME_CONDITION == "PAUSE":
            """
            Waiting for pressing the continue button
            """
            pass

        game.draw_screen(snake)


def start_game():
    while True:
        show_menu_screen()
        run_game()


if __name__ == '__main__':
    if DEBUG:
        start_test_game()
        import pygame
        pygame.init()
    else:
        start_game()
