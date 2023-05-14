import math
from base_objects import Cost, ShopItem, ShopItemType

from utils import INITIAL_BALANCE, INITIAL_MPT, INITIAL_PPT, GOAL_BALANCE


class Player:
    def __init__(self) -> None:
        self.balance = INITIAL_BALANCE
        self.mpt = INITIAL_MPT
        self.ppt = INITIAL_PPT
        self.inventory: list[ShopItem] = []

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

    def set_balance(self, set_to: float):
        self.balance = set_to

    def update(self):
        extra_mpt = 0
        extra_ppt = 0
        for inv_item in self.inventory:
            if inv_item.type_ == ShopItemType.AMULET or inv_item.type_ == ShopItemType.BUSINESS:
                extra_mpt += inv_item.mpt # type: ignore
                extra_ppt += inv_item.ppt # type: ignore
        self.mpt = INITIAL_MPT + extra_mpt
        self.ppt = INITIAL_PPT + extra_ppt
