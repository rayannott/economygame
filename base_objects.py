from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from copy import copy

from utils import COST_INCREASE_PER_TICK


class ShopItemType(Enum):
    '''
    Enumerator object for profit generator types
    '''
    AMULET = 'amulet'
    BUSINESS = 'business'
    EFFECT = 'effect'


@dataclass
class Cost:
    money: float
    balance_portion: float = 0.0

    def __str__(self) -> str:
        return f'{int(self.money)}, {self.balance_portion:.0%}'


class ShopItem(ABC):
    def __init__(self, name: str, cost: Cost, type_: ShopItemType) -> None:
        super().__init__()
        self.name = name
        self.cost = cost
        self.type_ = type_
        self.cost_increase_mult = 1
        self.per_purchase_portion_increase = 0.01 # increase of the Cost.balance_portion after every purchase, percent
        self.per_purchase_cost_mult = 1.05 # increase of the Cost.money after every purchase, multiple
        self.info: list[str] = []
    
    def tick(self):
        pass

    def __eq__(self, other: 'ProfitGen') -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
    
    def __repr__(self) -> str:
        return f'ShopItem::{self.name}'


class ProfitGen(ShopItem):
    def __init__(self, name: str, cost: Cost, type_: ShopItemType, mpt: float = 0, ppt: float = 0) -> None:
        '''
        Base abstract class for all profit generating items like amulets and businesses
        type_: type -- either AMULET or BUSINESS
        mps: money per tick bonus
        pps: per cent per tick bonus
        '''
        super().__init__(name, cost, type_)
        self.mpt = mpt
        self.ppt = ppt
    
    def tick(self):
        pass


class Effect(ShopItem):
    def __init__(self, name: str, cost: Cost, type_: ShopItemType, duration: float) -> None:
        super().__init__(name, cost, type_)
        self.DURATION = duration # constant
        self.duration = duration
        self.is_active = True
    
    def tick(self):
        if self.is_active:
            self.duration -= 1
            if self.duration == 0:
                self.is_active = False

    def __repr__(self) -> str:
        return f'Effect::{self.name}({self.duration} tx left)'


class ShopCell(ABC):
    def __init__(self, what: ShopItem) -> None:
        super().__init__()
        self.what = what
        self.item_cost = copy(what.cost)
    
    def tick(self):
        new_val = self.item_cost.money + COST_INCREASE_PER_TICK * self.what.cost_increase_mult
        if new_val >= 50:
            self.item_cost.money = new_val
    
    def __str__(self) -> str:
        return f'ShopCell({self.what} for {self.item_cost})'
    

class Shop:
    def __init__(self, items_to_add: list[ShopCell]) -> None:
        self.items: dict[str, ShopCell] = {}
        for item_to_add in items_to_add:
            self.items[item_to_add.what.name] = item_to_add

    def tick(self):
        for item in self.items.values():
            item.tick()
    
    def __getitem__(self, key):
        return self.items[key]
