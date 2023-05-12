from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

from utils import COST_INCREASE_PER_TICK

class PGType(Enum):
    '''
    Enumerator object for profit generator types
    '''
    AMULET = 'amulet'
    BUSINESS = 'business'


@dataclass
class Cost:
    money: float
    balance_portion: float = 0.0


class ShopItem(ABC):
    def __init__(self, name: str, cost: Cost) -> None:
        super().__init__()
        self.name = name
        self.cost = cost
    
    def tick(self):
        pass


class ProfitGen(ShopItem):
    def __init__(self, name: str, cost: Cost, pgtype: PGType, mps: float = 0, pmps: float = 0) -> None:
        '''
        Base abstract class for all profit generating items like amulets and businesses
        pgtype: type -- either AMULET or BUSINESS
        mps: money per second bonus
        pps: per-mille per second bonus
        '''
        super().__init__(name, cost)
        self.pgtype = pgtype
        self.mps = mps
        self.pmps = pmps
    
    def tick(self):
        pass


class Effect(ShopItem):
    def __init__(self, name: str, cost: Cost, duration: float) -> None:
        super().__init__(name, cost)
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
    

@dataclass
class Shop:
    items: list[ShopCell]

    def tick(self):
        for item in self.items:
            item.what.cost.money += COST_INCREASE_PER_TICK