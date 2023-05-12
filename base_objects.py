from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

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


class ShopItem(ABC):
    def __init__(self, name: str, cost: Cost, type_: ShopItemType) -> None:
        super().__init__()
        self.name = name
        self.cost = cost
        self.in_shop = True # cost increaing
        self.info = []
    
    def tick(self):
        pass


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
        self.duration = duration
        self.is_active = True
    
    def tick(self):
        if self.is_active:
            self.duration -= 1
            if self.duration == 0:
                self.is_active = False



class ShopCell(ABC):
    def __init__(self, what: ShopItem) -> None:
        super().__init__()
        self.what = what
    
    def tick(self):
        self.what.cost.money += COST_INCREASE_PER_TICK
    

@dataclass
class Shop:
    items: list[ShopCell]

    def tick(self):
        for item in self.items:
            item.tick()
