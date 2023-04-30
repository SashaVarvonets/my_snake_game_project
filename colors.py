import pygame


def get_color(*rgb):
    return pygame.Color(*rgb)


# Colors RGB
red = get_color(255, 0, 0)  # Game over
green = get_color(0, 255, 0)  # Snake body
dark_green = get_color(0, 100, 0)  # Snake head
black = get_color(0, 0, 0)  # Score and level
white = get_color(240, 255, 255)  # Background
brown = get_color(165, 42, 42)  # Food
grey = get_color(40, 40, 40)  # Border
grey_1 = get_color(41, 40, 40)  # Border
