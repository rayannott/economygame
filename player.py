from collections import defaultdict, deque
from copy import deepcopy
from dataclasses import dataclass
import math

from base_objects import Cost, Effect, ShopCell, ShopItem, ShopItemType
from shop_items import Bakery, SouvenirShop, BoostPpt
from utils import INITIAL_BALANCE, INITIAL_MPT, INITIAL_PPT, GOAL_BALANCE, AVAILABLE_EFFECTS_SLOTS, BONUS_AMOUNT, BONUS_EVERY, PER_BAKERY_EFFECT_BOOST

@dataclass
class EffectFlags:
    boost_ppt: bool = False
    boost_mpt: bool = False
    mega_stocks: bool = False
    evilwizardry: bool = False

class Player:
    def __init__(self) -> None:
        self.balance = INITIAL_BALANCE
        self.mpt = INITIAL_MPT
        self.ppt = INITIAL_PPT
        self.effect_duration_boost = 0
        self.inventory: list[ShopItem] = []
        self.effects: list[Effect | None] = [None] * AVAILABLE_EFFECTS_SLOTS
        self.effect_flags: EffectFlags = EffectFlags()
        self.times_ticked = 0
        self.extra_mpt = [0., 0.] # amulets, businesses
        self.extra_ppt = [0., 0.] # amulets, businesses

        self.spent_on_each_shop_item: dict[str, deque[float]] = defaultdict(deque) # holds a history of spendings to enable selling
        self.INITIAL_TIME_UNTIL_VICTORY = self.time_until_victory()
        self.do_nothing_balance = INITIAL_BALANCE

    def tick(self):
        # account for effects:
        self.times_ticked += 1
        self.effect_flags = EffectFlags()
        for eff in self.effects:
            if eff is None:
                continue
            if eff.name == 'Boost PPT':
                self.effect_flags.boost_ppt = True
            elif eff.name == 'Boost MPT':
                self.effect_flags.boost_mpt = True
            elif eff.name == 'Mega Stocks':
                self.effect_flags.mega_stocks = True
            elif eff.name == 'Evil Wizardry':
                self.effect_flags.evilwizardry = True

        # update balance:
        stocks_mult = 2.5 if self.effect_flags.mega_stocks else 1
        evilwizardry = 2.5 if self.effect_flags.evilwizardry else 1
        boost_ppt_mult = 3 if self.effect_flags.boost_ppt else 1
        boost_mpt_mult = 3 if self.effect_flags.boost_mpt else 1
        
        self.real_ppt = (INITIAL_PPT + self.extra_ppt[0] * evilwizardry + self.extra_ppt[1] * stocks_mult) * boost_ppt_mult
        self.real_mpt = (INITIAL_MPT + self.extra_mpt[0] * evilwizardry + self.extra_mpt[1] * stocks_mult) * boost_mpt_mult
        self.balance *= 1 + self.real_mpt * 0.01
        self.balance += self.real_mpt

        # update fake balance to keep track of how well we're doing
        self.do_nothing_balance *= 1+INITIAL_PPT*0.01
        self.do_nothing_balance += INITIAL_MPT
        if self.times_ticked % BONUS_EVERY == 0: self.do_nothing_balance += BONUS_AMOUNT

        # update effects:
        zero_duration_ids = []
        for i, eff in enumerate(self.effects):
            if eff is not None:
                eff.tick()
                if eff.duration == 0:
                    zero_duration_ids.append(i)
        for idx in zero_duration_ids:
            self.effects[idx] = None
            print(f'effect {idx} terminated')
            


    def time_until_victory(self) -> float:
        return math.log((GOAL_BALANCE + 100*self.mpt/(self.ppt))/(self.balance + 100*self.mpt/(self.ppt)), 1+self.ppt*0.01)

    def do_nothing_time_until_victory(self) -> float:
        return math.log(
            (GOAL_BALANCE + 100*INITIAL_MPT/(INITIAL_PPT))/(self.do_nothing_balance + 100*INITIAL_MPT/(INITIAL_PPT)), 
            1+INITIAL_PPT*0.01
        )

    def enough_money(self, cost: Cost) -> tuple[bool, float]:
        '''
        Checks if there's enough balance to buy something.
        Returns a tuple (is_possible_to_buy flag, resulting balance if true)
        '''
        resulting_balance = self.balance * (1 - cost.balance_portion) - cost.money
        if resulting_balance >= 0:
            return True, resulting_balance
        return False, 0.
    
    def buy_shop_cell(self, shop_cell: ShopCell) -> tuple[bool, str]:
        '''Buys an item; returns (True, '') if success, else (False, message)'''
        is_possible_to_buy, resulting_balance = self.enough_money(shop_cell.item_cost)
        if is_possible_to_buy:
            spent = self.balance - resulting_balance
            if shop_cell.what.type_ == ShopItemType.EFFECT:
                if all(self.effects):
                    return False, 'all effect slots\nare occupied'
                none_index = -1
                for i, eff in enumerate(self.effects): 
                    if eff is None: none_index = i; break
                self.effects[none_index] = deepcopy(shop_cell.what) # type: ignore
                self.effects[none_index].duration += self.effect_duration_boost # type: ignore
            else:
                self.inventory.append(shop_cell.what)
                self.spent_on_each_shop_item[shop_cell.what.name].append(spent)
            
            self.set_balance(resulting_balance)
            shop_cell.item_cost = Cost(
                money=shop_cell.item_cost.money * shop_cell.what.per_purchase_cost_mult, 
                balance_portion=min(shop_cell.item_cost.balance_portion + shop_cell.what.per_purchase_portion_increase, 0.5)
            )
            return True, ''
        return False, 'not enough money'

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
        self.set_balance(self.balance + spent)
        return True

    def set_balance(self, set_to: float):
        self.balance = set_to

    def update(self):
        amulets = 0
        for inv_item in self.inventory:
            if inv_item.type_ == ShopItemType.AMULET:
                amulets += 1


        self.extra_mpt = [0., 0.]
        self.extra_ppt = [0., 0.]

        self.effect_duration_boost = 0

        for inv_item in self.inventory:
            if inv_item.type_ == ShopItemType.AMULET:
                self.extra_mpt[0] += inv_item.mpt # type: ignore
                self.extra_ppt[0] += inv_item.ppt # type: ignore
                pass
            elif inv_item.type_ == ShopItemType.BUSINESS:
                if isinstance(inv_item, SouvenirShop):
                    self.extra_mpt[1] += inv_item.mpt * amulets
                    continue
                elif isinstance(inv_item, Bakery):
                    self.effect_duration_boost += PER_BAKERY_EFFECT_BOOST
                self.extra_mpt[1] += inv_item.mpt # type: ignore
                self.extra_ppt[1] += inv_item.ppt # type: ignore

        self.mpt = INITIAL_MPT + sum(self.extra_mpt)
        self.ppt = INITIAL_PPT + sum(self.extra_ppt)
