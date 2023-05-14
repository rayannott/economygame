from collections import defaultdict, deque
import math
from base_objects import Cost, ShopCell, ShopItem, ShopItemType
from shop_items import Bakery, SouvenirShop

from utils import INITIAL_BALANCE, INITIAL_MPT, INITIAL_PPT, GOAL_BALANCE


class Player:
    def __init__(self) -> None:
        self.balance = INITIAL_BALANCE
        self.mpt = INITIAL_MPT
        self.ppt = INITIAL_PPT
        self.effect_duration_boost = 0
        self.inventory: list[ShopItem] = []
        self.spent_on_each_shop_item: dict[str, deque[float]] = defaultdict(deque)

    def tick(self):
        self.balance *= 1+self.ppt*0.01
        self.balance += self.mpt

    def time_until_victory(self) -> float:
        return math.log((GOAL_BALANCE + 100*self.mpt/(self.ppt))/(self.balance + 100*self.mpt/(self.ppt)), 1+self.ppt*0.01)

    def enough_money(self, cost: Cost) -> tuple[bool, float]:
        '''
        Checks if there's enough balance to buy something.
        Returns a tuple (is_possible_to_buy flag, resulting balance if true)
        '''
        resulting_balance = self.balance * (1 - cost.balance_portion) - cost.money
        if resulting_balance >= 0:
            return True, resulting_balance
        return False, 0.
    
    def buy_shop_cell(self, shop_cell: ShopCell) -> bool:
        '''Buys an item; returns True if success, else False'''
        is_possible_to_buy, resulting_balance = self.enough_money(shop_cell.item_cost)
        if is_possible_to_buy:
            self.inventory.append(shop_cell.what)
            spent = self.balance - resulting_balance
            self.set_balance(resulting_balance)
            self.spent_on_each_shop_item[shop_cell.what.name].append(spent)
            shop_cell.item_cost = Cost(money=shop_cell.item_cost.money*1.1, balance_portion=shop_cell.item_cost.balance_portion + 0.01)
            return True
        return False

    def sell_item(self, item_name: str) -> bool:
        '''
        Tries to sell an item with a given name.
        If successful, return True; else, False.
        '''
        if not self.spent_on_each_shop_item.get(item_name):
            return False
        
        index_to_pop = None
        for i, inv_item in enumerate(self.inventory):
            if inv_item.name == item_name:
                index_to_pop = i
                break
        assert index_to_pop is not None
        self.inventory.pop(index_to_pop)
        spent = self.spent_on_each_shop_item[item_name].popleft()
        self.set_balance(self.balance + spent * 0.5)
        return True

    def set_balance(self, set_to: float):
        self.balance = set_to

    def update(self):
        amulets = 0
        for inv_item in self.inventory:
            if inv_item.type_ == ShopItemType.AMULET:
                amulets += 1

        extra_mpt = 0
        extra_ppt = 0
        self.effect_duration_boost = 0
        for inv_item in self.inventory:
            if inv_item.type_ == ShopItemType.AMULET or inv_item.type_ == ShopItemType.BUSINESS:
                if isinstance(inv_item, SouvenirShop):
                    extra_mpt += inv_item.mpt * amulets
                    continue
                elif isinstance(inv_item, Bakery):
                    self.effect_duration_boost += 1
                
                extra_mpt += inv_item.mpt # type: ignore
                extra_ppt += inv_item.ppt # type: ignore
        
        self.mpt = INITIAL_MPT + extra_mpt
        self.ppt = INITIAL_PPT + extra_ppt
