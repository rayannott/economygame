import pygame

from game import Game
from sfx_tools import set_sfx_volume, DEFAULT_SFX_VOLUME

pygame.init()
set_sfx_volume(DEFAULT_SFX_VOLUME)

if __name__ == '__main__':
    game = Game()
    game.run()
