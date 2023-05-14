import pygame

from base_objects import ProfitGen, ShopCell, ShopItem, Shop
from gui.gui_utils import CP1, FONT_SMALL, FONT_NORM, WHITE, SHOP_ITEM_PANEL_SIZE, BUY_BTN_SIZE
from gui.gui_rect import Panel, Label, Button


TOPLEFTS = []
for i in range(4):
    for j in range(4):
        TOPLEFTS.append(
            (4*(j+1) + SHOP_ITEM_PANEL_SIZE[0]*j, 30 + 4*i + SHOP_ITEM_PANEL_SIZE[1]*i)
        )


def create_panels_from_shop(shop: Shop, surface: pygame.Surface, shop_panel: Panel) -> dict[str, Panel]:
    to_ret = {}
    for i, sh_item in enumerate(shop.items.values()):
        pnl = Panel(topleft=TOPLEFTS[i], size=SHOP_ITEM_PANEL_SIZE, surface=surface, hoverhint=sh_item.what.name, parent=shop_panel)
        pnl.add_labels(
            [Label(f'[{sh_item.what.name}]', surface, FONT_NORM, CP1[0], topleft=(2, 2)),
             Label(f'{sh_item.what.type_.name[0]}', surface, FONT_NORM, color=CP1[1], bottomleft=(2, SHOP_ITEM_PANEL_SIZE[1]-2))]
        )
        for i, info in enumerate(sh_item.what.info, 1):
            pnl.add_labels(
                [Label(info, surface, FONT_SMALL, WHITE, topleft=(15, 10 + 24*i))]
            )
        pnl.populate_one(
            'buy',
            Button(
                (SHOP_ITEM_PANEL_SIZE[0] - BUY_BTN_SIZE[0] - 4, SHOP_ITEM_PANEL_SIZE[1] - BUY_BTN_SIZE[1] - 4), 
                BUY_BTN_SIZE, surface, str(sh_item.item_cost), f'buy {sh_item.what.name}', text_font=FONT_SMALL, parent=pnl
            )
        )
        to_ret[sh_item.what.name] = pnl
    return to_ret
