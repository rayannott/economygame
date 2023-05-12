from typing import Type

import pygame

from base_objects import ProfitGen, ShopCell, ShopItem
from gui.pygame_utils import CP1, FONT_SMALL, WHITE
from gui.gui_rect import Panel, Label, Button

# class ShopItemPanel(Panel):
#     def __init__(self, topleft: tuple[float, float], 
#                 size: tuple[float, float], surface: pygame.Surface,
#                 shop_panel: Panel,
#                 shop_item: ShopItem,
#                 requires_clarification: bool = False,
#                 hoverhint: str = '',
#                 ) -> None:
#         super().__init__(topleft, size, surface, hoverhint, shop_panel)
#         self.requires_clarification = requires_clarification
#         self.shop_item = shop_item

# def create_shop_item_panel(shop_item: ShopItem, info: str, hoverhint: str,
#                       req_clarification: bool,
#                       topleft: tuple[int, int], surface, shop_panel):
#     pnl = ShopItemPanel(topleft, (300, 280), surface, shop_panel, shop_item, req_clarification, hoverhint)
#     pnl.add_labels([
#         Label(shop_item.name, surface, FONT_SMALL, CP1[0], topleft=(4, 4)),
#         Label(info, surface, FONT_SMALL, WHITE, topleft=(4, 24)),
#         Label(f'cost: {shop_item.cost}', surface, FONT_SMALL, WHITE, topleft=(4, 200))
#         ]
#     )
#     pnl.populate_one(
#         'buy',
#         Button((40, 230), (120, 40), surface, 'BUY', f'buy {shop_item.name}', FONT_SMALL, pnl)
#     )
#     return pnl

