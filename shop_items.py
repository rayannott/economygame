from base_objects import Cost, Shop, ShopCell, ShopItem, ProfitGen, ShopItemType, Effect
from utils import PER_BAKERY_EFFECT_BOOST


class IronNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Iron Nugget', cost=Cost(50., 0.1), type_=ShopItemType.AMULET, mpt=-0.05, ppt=0.02)
        self.info = [f'+{self.ppt} ppt', f'{self.mpt} mpt'] # a list of strings to display on ShopItemPanel
        self.per_purchase_cost_mult = 1.1
        self.per_purchase_portion_increase = 0.02


class CopperNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Copper Nugget', cost=Cost(400., 0.), type_=ShopItemType.AMULET, mpt=0., ppt=0.06)
        self.info = [f'+{self.ppt} ppt', '(cost dec 5x)', '(each purchase -10%)']
        self.cost_increase_mult = -5
        self.per_purchase_cost_mult = 0.9
        self.per_purchase_portion_increase = 0


class GoldenNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Golden Nugget', cost=Cost(600., 0.03), type_=ShopItemType.AMULET, mpt=0.4, ppt=0.12)
        self.info = [f'+{self.ppt} ppt', f'+{self.mpt} mpt', '(cost inc 0x)']
        self.cost_increase_mult = 0


class Bakery(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Bakery', cost=Cost(340., 0.05), type_=ShopItemType.BUSINESS, mpt=0.4, ppt=0)
        self.info = [f'+{self.mpt} mpt', f'+{PER_BAKERY_EFFECT_BOOST} tx effects duration']


class SouvenirShop(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Souvenir Shop', cost=Cost(140., 0.2), type_=ShopItemType.BUSINESS, mpt=0.15, ppt=0)
        self.info = [f'+{self.mpt} x (# amulets) mpt']
        self.per_purchase_cost_mult = 1.1
        self.per_purchase_portion_increase = 0.02


class BoostPpt(Effect):
    def __init__(self) -> None:
        super().__init__(name='Boost PPT', cost=Cost(190., 0.), type_=ShopItemType.EFFECT, duration=15)
        self.info = ['3 x (ppt)', f'for {self.duration} sec', '(cost inc 0.5x)']
        self.cost_increase_mult = 0.5


class BoostMpt(Effect):
    def __init__(self) -> None:
        super().__init__(name='Boost MPT', cost=Cost(20., 0.2), type_=ShopItemType.EFFECT, duration=15)
        self.info = ['3 x (mpt)', f'for {self.duration} sec', '(cost inc 3x)', '(each purchase +50%)']
        self.cost_increase_mult = 3


class MegaStocks(Effect):
    def __init__(self) -> None:
        super().__init__(name='Mega Stocks', cost=Cost(350., 0.02), type_=ShopItemType.EFFECT, duration=15)
        self.info = ['2.5 x (mpt), 2.5 x (ppt)', 'of all businesses', f'for {self.duration} sec']


class EvilWizardry(Effect):
    def __init__(self) -> None:
        super().__init__(name='Evil Wizardry', cost=Cost(120., 0.2), type_=ShopItemType.EFFECT, duration=15)
        self.info = ['2.5 x (mpt), 2.5 x (ppt)', 'of all amulets', f'for {self.duration} sec']


def create_shop() -> Shop:
    return Shop(
        [
            ShopCell(IronNugget()),
            ShopCell(CopperNugget()),
            ShopCell(GoldenNugget()),
            ShopCell(Bakery()),
            ShopCell(SouvenirShop()),
            ShopCell(BoostPpt()),
            ShopCell(BoostMpt()),
            ShopCell(MegaStocks()),
            ShopCell(EvilWizardry())
        ]
    )
