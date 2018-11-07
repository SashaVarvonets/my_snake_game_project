import pygame
from functions import show_menu_screen, run_game


if __name__ == '__main__':

    pygame.init()
    pygame.display.set_caption('Snake Game')

    while True:
        show_menu_screen()
        run_game()
