import pygame

WHITE = '#FFFFFF'
BLACK = '#000000'
GREY = '#333333'
CP0 = ('#DB5294', '#52DB9A') # cool color pair number 0
CP1 = ('#AE5DDA', '#89DA5D')


pygame.font.init()
FONT_HINT = pygame.font.Font('main_font.ttf', 14)
FONT_NORM = pygame.font.Font('main_font.ttf', 20)
FONT_HUGE = pygame.font.Font('main_font.ttf', 34)

WINDOW_SIZE = (1200, 800)
FRAMERATE = 60

def shift(tup1: tuple, tup2: tuple) -> tuple:
    return tup1[0] + tup2[0], tup1[1] + tup2[1]