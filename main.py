import pygame

from gui.gui_rect import Button, ProgressBar, Panel
from gui.pygame_utils import BLACK, FRAMERATE, WINDOW_SIZE, FONT_HUGE, FONT_HINT, CP0
from game import Game


pygame.init()


if __name__ == '__main__':
    game = Game()
    game.run()
