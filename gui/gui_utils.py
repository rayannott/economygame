import pygame

WHITE = '#FFFFFF'
BLACK = '#000000'
GREY = '#333333'
GREEN = '#00FF00'
RED = '#FF0000'
CP0 = ('#DB5294', '#52DB9A') # cool color pair number 0
CP1 = ('#AE5DDA', '#89DA5D')


pygame.font.init()
FONT_SMALL = pygame.font.Font('main_font.ttf', 14)
FONT_NORM = pygame.font.Font('main_font.ttf', 20)
FONT_HUGE = pygame.font.Font('main_font.ttf', 34)

WINDOW_SIZE = (1200, 800)
INFO_PANEL_SIZE = (300, 240)
SHOP_PANEL_SIZE = (WINDOW_SIZE[0] - INFO_PANEL_SIZE[0] - 10, WINDOW_SIZE[1] - 25)
INVENTORY_PANEL_SIZE = (INFO_PANEL_SIZE[0], 320)
EFFECTS_PANEL_SIZE = (INFO_PANEL_SIZE[0], WINDOW_SIZE[1] - INFO_PANEL_SIZE[1] - INVENTORY_PANEL_SIZE[1] - 31)
FRAMERATE = 60

SHOP_ITEM_PANEL_SIZE = (217, 188)
BUY_BTN_SIZE = (100, 40)

INV_BTN_SLOT_SIZE = (260, 40)

def shift(tup1: tuple, tup2: tuple) -> tuple:
    return tup1[0] + tup2[0], tup1[1] + tup2[1]
