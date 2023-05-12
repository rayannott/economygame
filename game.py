

import time
import pygame

from player import Player
from gui.gui_rect import Button, Label, ProgressBar, Panel
from gui.pygame_utils import BLACK, FONT_NORM, FRAMERATE, WHITE, WINDOW_SIZE, FONT_HUGE, FONT_SMALL, CP0
from shop_items import *
from utils import TICK


class Game:
    def __init__(self) -> None:
        pygame.init()

        self.player = Player()
        self.current_time = time.time()
        self.time_of_last_tick = 0
        self.times_ticked = 0
        self.victory = False
        self.paused = False

        # setup pygame
        pygame.display.set_caption('Game')
        self.surface = pygame.display.set_mode(WINDOW_SIZE)

        self.background = pygame.Surface(WINDOW_SIZE)
        self.background.fill(pygame.Color(BLACK))

        self.clock = pygame.time.Clock()

        self.is_running = True


        # setup GUIs

        self.info_panel = Panel((3, 3), (300, 240), self.surface, 'info')
        self.info_panel.add_labels(
            [
                Label('Info', self.surface, FONT_NORM, CP0[1], topleft=(45, 3)),
                Label(f'time: {self.times_ticked} tx', self.surface, FONT_NORM, WHITE, topleft=(6, 28)),
                Label(f'balance: {self.player.balance:.1f}', self.surface, FONT_NORM, WHITE, topleft=(6, 53)),
                Label(f'[until victory: {self.player.time_until_victory():.0f} tx]', self.surface, FONT_SMALL, WHITE, topleft=(15, 78)),
                Label(f'mpt: {self.player.mpt}', self.surface, FONT_NORM, WHITE, topleft=(6, 103)),
                Label(f'ppt: {self.player.ppt}', self.surface, FONT_NORM, WHITE, topleft=(6, 128)),
            ]
        )
        self.info_panel.populate_one(
            'pause_btn',
            Button((40, 200), (100, 24), self.surface, 'pause', 'toggle pause/unpause', parent=self.info_panel)
        )
        

        self.inventory_panel = Panel((3, 246), (300, WINDOW_SIZE[1] - 268), self.surface, 'inv')
        self.inventory_panel.add_labels([
            Label('Inventory', self.surface, FONT_NORM, CP0[1], topleft=(45, 3))
        ])


        self.shop_panel = Panel((306, 3), (WINDOW_SIZE[0] - 310, WINDOW_SIZE[1] - 25), self.surface, 'shop')

        self.shop_item_panels = []

        self.shop_panel.add_labels(
            [Label('Shop', self.surface, FONT_NORM, CP0[1], topleft=(45, 3))]
        )

    def update(self):
        '''Updates the brains of the game (back)'''
        self.current_time = time.time()
        if self.current_time - self.time_of_last_tick > TICK:
            self.tick()
            self.time_of_last_tick = self.current_time
        
        # labels:
        self.info_panel.labels[1].set_text(f'time: {self.times_ticked} tx')
        self.info_panel.labels[2].set_text(f'balance: {self.player.balance:.1f}')
        self.info_panel.labels[3].set_text(f'[until victory: {self.player.time_until_victory():.0f} tx]')

    def run(self):
        '''
        Infinite game loop
        '''
        while self.is_running:
            if not self.paused:
                self.update() # update the game data (back)
            
            self.clock.tick(FRAMERATE)
            self.surface.blit(self.background, (0, 0))
            pos = pygame.mouse.get_pos()

            self.info_panel.update(pos)
            self.inventory_panel.update(pos)
            self.shop_panel.update(pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.info_panel.clicked():
                        if self.info_panel.gui_objects['pause_btn'].clicked():
                            self.paused = not self.paused


            pygame.display.update()

    def tick(self):
        '''
        This function is executed every TICK
        '''
        self.times_ticked += 1
        self.player.tick()
