from collections import Counter
import time

import pygame

from base_objects import Cost, ShopCell, ShopItemType
from player import Player
from gui.gui_rect import Button, Label, Notification, ProgressBar, Panel
from gui.gui_utils import BLACK, CP1, EFFECTS_PANEL_SIZE, FONT_NORM, FRAMERATE, GREEN, INFO_PANEL_SIZE, INVENTORY_PANEL_SIZE, RED, SHOP_PANEL_SIZE, WHITE, WINDOW_SIZE, FONT_HUGE, FONT_SMALL, CP0, INV_BTN_SLOT_SIZE, random_point
from gui.gui_shop import create_panels_from_shop
import shop_items as si
from shop_items import create_shop
from utils import BONUS_AMOUNT, BONUS_EVERY, GOAL_BALANCE, SELL_ITEM_ORIGINAL_PRICE_PORTION, TICK


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
        self.notifications: list[Notification] = []

        self.info_panel = Panel((3, 3), INFO_PANEL_SIZE, self.surface, 'info')
        tuv = self.player.time_until_victory()
        self.info_panel.add_labels(
            [
                Label('Info', self.surface, FONT_NORM, CP0[1], topleft=(45, 3)),
                Label(f'time: {self.times_ticked} tx', self.surface, FONT_NORM, WHITE, topleft=(6, 28)),
                Label(f'balance: {self.player.balance:.1f}', self.surface, FONT_NORM, WHITE, topleft=(6, 53)),
                Label(f'[until victory: {tuv:.0f} tx]', self.surface, FONT_SMALL, WHITE, topleft=(15, 78)),
                Label(f'{self.player.do_nothing_time_until_victory() - tuv:.0f}', self.surface, FONT_SMALL, WHITE, topleft=(220, 78)),
                Label(f'mpt: {self.player.mpt:.2f}', self.surface, FONT_NORM, WHITE, topleft=(6, 103)),
                Label(f'ppt: {self.player.ppt:.2f}', self.surface, FONT_NORM, WHITE, topleft=(6, 128)),
            ]
        )
        self.info_panel.populate_one(
            'pause_btn',
            Button((40, 200), (100, 24), self.surface, 'pause', 'toggle pause/unpause', parent=self.info_panel)
        )
        self.info_panel.populate_one(
            'debug_btn',
            Button((150, 200), (24, 24), self.surface, 'd', 'debug button', parent=self.info_panel)
        )

        self.inventory_panel = Panel((3, INFO_PANEL_SIZE[1] + 6), INVENTORY_PANEL_SIZE, self.surface, 'inv')
        self.inventory_panel.add_labels([
            Label('Inventory', self.surface, FONT_NORM, CP0[1], topleft=(45, 3))
        ])
        self.next_empty_slot_index = 0

        self.effects_panel = Panel((3, INFO_PANEL_SIZE[1] + INVENTORY_PANEL_SIZE[1] + 9), EFFECTS_PANEL_SIZE, self.surface, 'effects')
        self.effects_panel.add_labels(
            [Label('Effects', self.surface, FONT_NORM, CP0[1], topleft=(45, 3))]
        )
        self.effect_slots = [False, False, False] # three empty slots

        self.shop_panel = Panel((INFO_PANEL_SIZE[0] + 6, 3), SHOP_PANEL_SIZE, self.surface, 'market')
        self.shop_panel.add_labels(
            [Label('Market', self.surface, FONT_NORM, CP0[1], topleft=(45, 3))]
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
        
        self.player.update()
        if self.player.balance >= GOAL_BALANCE and not self.victory:
            self.victory = True
            self.spawn_notification(f'You won @ \n {self.times_ticked} tx', (WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
            print(f'won @ {self.times_ticked} tx')
            self.info_panel.add_labels(
                [Label(f'won @ {self.times_ticked} tx', self.surface, FONT_NORM, CP0[0], topleft=(6, 153))]
            )
            self.info_panel.labels[3].deactivate()
            self.info_panel.labels[4].deactivate()
            
    
    def update_gui(self, current_mouse_pos: tuple[int, int]):
        # info panel:
        self.info_panel.labels[1].set_text(f'time: {self.times_ticked} tx')
        self.info_panel.labels[2].set_text(f'balance: {self.player.balance:.1f}')
        tuv = self.player.time_until_victory()
        self.info_panel.labels[3].set_text(f'[until victory: {tuv:.0f} tx]')
        winning_by = self.player.do_nothing_time_until_victory() - tuv
        self.info_panel.labels[4].set_text(f'{winning_by:.0f}')
        self.info_panel.labels[4].set_color(GREEN if winning_by >= 0 else RED)
        self.info_panel.labels[5].set_text(f'mpt: {self.player.mpt:.2f} (real {self.player.real_mpt:.2f})')
        self.info_panel.labels[6].set_text(f'ppt: {self.player.ppt:.2f} (real {self.player.real_ppt:.2f})')

        self.info_panel.update(current_mouse_pos)

        # shop panel:
        for key, shop_panel_item in self.shop_panel.gui_objects.items():
            item_cost = self.shop[key].item_cost
            shop_panel_item.gui_objects['buy'].set_text(str(item_cost)) # type: ignore
            can_buy, res_balance = self.player.enough_money(item_cost)
            frame_color = WHITE if can_buy else RED
            shop_panel_item.gui_objects['buy'].set_frame_color(frame_color) # type: ignore
            hoverhint_text = f'buy for {self.player.balance - res_balance:.0f}' if can_buy else f'cannot buy: need at least {item_cost.money / (1-item_cost.balance_portion):.0f}'
            shop_panel_item.gui_objects['buy'].hint_label.set_text(hoverhint_text) # type: ignore
        
        self.shop_panel.update(current_mouse_pos)

        # inventory slots:
        for inv_item in set(self.player.inventory):
            if inv_item.name not in self.inventory_panel.gui_objects:
                self.inventory_panel.populate_one(
                    inv_item.name,
                    Button(
                        topleft=(5, (INV_BTN_SLOT_SIZE[1] + 3) * (self.next_empty_slot_index + 1)), 
                        size=INV_BTN_SLOT_SIZE, 
                        surface=self.surface, 
                        text=f'{inv_item.name} x ({len(self.player.spent_on_each_shop_item[inv_item.name])})',
                        hoverhint=f'sell {inv_item.name} for {self.player.spent_on_each_shop_item[inv_item.name][0]:.1f}',
                        parent=self.inventory_panel
                    )
                )
                self.next_empty_slot_index += 1
        for inv_name, inv_slot in self.inventory_panel.gui_objects.items():
            inv_slot.set_text(f'{inv_name} x ({len(self.player.spent_on_each_shop_item[inv_name])})')
            dq = self.player.spent_on_each_shop_item[inv_name]
            extra = f'for {dq[0] * SELL_ITEM_ORIGINAL_PRICE_PORTION:.1f}' if dq else '(currently unavailable)'
            inv_slot.hint_label.set_text(f'sell {inv_name} {extra}')
        self.inventory_panel.update(current_mouse_pos)

        # effects:
        for eff_idx, eff in enumerate(self.player.effects):
            if str(eff_idx) in self.effects_panel.gui_objects:
                if eff is None:
                    del self.effects_panel.gui_objects[str(eff_idx)]
                else: # updating the progressbar
                    self.effects_panel.gui_objects[str(eff_idx)].set_progress(eff.duration/eff.DURATION)  # type: ignore
                    self.effects_panel.gui_objects[str(eff_idx)].set_text(f'{eff.name} ({eff.duration})')  # type: ignore
            else:
                if eff is None:
                    continue
                self.effects_panel.populate_one(
                    str(eff_idx),
                    ProgressBar(
                        topleft=(15, (INV_BTN_SLOT_SIZE[1] + 3) * (eff_idx + 1)),
                        size=INV_BTN_SLOT_SIZE,
                        surface=self.surface,
                        progress=1.,
                        text=f'{eff.name} ()',
                        hoverhint='effect',
                        display_progress=False,
                        parent=self.effects_panel
                    )
                )
        self.effects_panel.update(current_mouse_pos)

        # notifications:
        for notif in self.notifications:
            notif.update(current_mouse_pos)

    def spawn_notification(self, text: str, pos: tuple[int, int], duration: int = 6):
        self.notifications.append(Notification(text, self.surface, pos=pos, duration_tics=duration))
    
    def buy_shop_cell(self, shop_cell: ShopCell) -> tuple[bool, str]:
        '''Buys an item; returns True if success, else False'''
        return self.player.buy_shop_cell(shop_cell)
    
    def sell_item(self, item_name: str) -> bool:
        return self.player.sell_item(item_name)

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

            # update gui
            self.update_gui(pos)

            # process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.info_panel.clicked():
                        if self.info_panel.gui_objects['pause_btn'].clicked():
                            if not self.paused:
                                self.spawn_notification('paused', pos, duration=1)
                            self.paused = not self.paused
                        elif self.info_panel.gui_objects['debug_btn'].clicked():
                            # DEBUG
                            print('DEB - inv:', self.player.inventory)
                            print('DEB - effects:', self.player.effects)
                            print('DEB - inv spending history:', self.player.spent_on_each_shop_item)
                            print('DEB - effect flags:', self.player.effect_flags)
                            print('DEB - real mpt, ppt:', self.player.real_mpt, self.player.real_ppt)
                            print('DEB - effect duration boost:', self.player.effect_duration_boost)

                    elif self.shop_panel.clicked():
                        what_clicked = self.shop_panel.object_clicked()
                        if what_clicked:
                            what_clicked_2 = self.shop_panel.gui_objects[what_clicked].object_clicked() # type: ignore
                            if what_clicked_2 == 'buy':
                                success, message = self.buy_shop_cell(self.shop[what_clicked])
                                if success:
                                    print(f'bought {self.shop[what_clicked]} @ {self.times_ticked} tx')
                                else:
                                    print(message.replace('\n', ' '))
                                    self.spawn_notification(message, pos, 1)

                    elif self.inventory_panel.clicked():
                        what_clicked = self.inventory_panel.object_clicked()
                        if what_clicked:
                            feedback = self.sell_item(what_clicked)
                            if feedback:
                                print(f'sold {what_clicked}')
                            else:
                                print(f'you don\'t have {what_clicked}')
                                self.spawn_notification(f'no {what_clicked} left', pos, 3)
            pygame.display.update()

    def tick(self):
        '''
        This function is executed every TICK
        '''
        self.times_ticked += 1
        self.player.tick()
        self.shop.tick()
        if self.times_ticked % BONUS_EVERY == 0:
            self.player.set_balance(self.player.balance + BONUS_AMOUNT)
            self.spawn_notification(f'you received a bonus: {BONUS_AMOUNT}', random_point())
        for notif in self.notifications:
            notif.tick()
