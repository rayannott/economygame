

import time
import pygame
from base_objects import ShopCell

from player import Player
from gui.gui_rect import Button, Label, ProgressBar, Panel
from gui.pygame_utils import BLACK, FONT_NORM, FRAMERATE, WHITE, WINDOW_SIZE, FONT_HUGE, FONT_SMALL, CP0
from gui.gui_shop import create_panels_from_shop
import shop_items as si
from shop_items import create_shop
from utils import TICK


class Game:
    def __init__(self) -> None:
        pygame.init()

        # setup back

        self.player = Player()
        self.current_time = time.time()
        self.time_of_last_tick = 0
        self.times_ticked = 0
        self.victory = False
        self.paused = False
        self.shop = create_shop()


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
                Label(f'mpt: {self.player.mpt:.3f}', self.surface, FONT_NORM, WHITE, topleft=(6, 103)),
                Label(f'ppt: {self.player.ppt:.3f}', self.surface, FONT_NORM, WHITE, topleft=(6, 128)),
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

        self.shop_panel.add_labels(
            [Label('Shop', self.surface, FONT_NORM, CP0[1], topleft=(45, 3))]
        )

        self.shop_panel.populate_many(
            create_panels_from_shop(self.shop, self.surface, self.shop_panel) # type: ignore
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
        self.info_panel.labels[4].set_text(f'mpt: {self.player.mpt:.3f}')
        self.info_panel.labels[5].set_text(f'ppt: {self.player.ppt:.3f}')

        for key, shop_panel_item in self.shop_panel.gui_objects.items():
            shop_panel_item.gui_objects['buy'].text_label.set_text(str(self.shop[key].item_cost)) # type: ignore
        
        self.player.update()

    def buy_shop_cell(self, shop_cell: ShopCell) -> bool:
        '''Buys an item; returns True if success, else False'''
        is_possible_to_buy, resulting_balance = self.player.enough_money(shop_cell.item_cost)
        if is_possible_to_buy:
            self.player.inventory.append(shop_cell.what)
            self.player.set_balance(resulting_balance)
            return True
        return False

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
                    if self.shop_panel.clicked():
                        print('shop panel')
                        what_clicked = self.shop_panel.object_clicked()
                        if what_clicked:
                            print(f'    clicked {what_clicked}')
                            what_clicked_2 = self.shop_panel.gui_objects[what_clicked].object_clicked() # type: ignore
                            if what_clicked_2 == 'buy':
                                feedback = self.buy_shop_cell(self.shop[what_clicked])
                                if feedback:
                                    print(f'        bought {what_clicked}: {self.shop[what_clicked]}')
                                else:
                                    print('        not enough money')


            pygame.display.update()

    def tick(self):
        '''
        This function is executed every TICK
        '''
        self.times_ticked += 1
        self.player.tick()
        self.shop.tick()
