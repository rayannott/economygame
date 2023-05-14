from base_objects import Cost, Shop, ShopCell, ShopItem, ProfitGen, ShopItemType, Effect


class IronNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Iron Nugget', cost=Cost(150., 0.), type_=ShopItemType.AMULET, mpt=0., ppt=0.01)
        self.info = [f'+{self.ppt} ppt'] # a list of strings to display on ShopItemPanel


class CopperNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Copper Nugget', cost=Cost(600., 0), type_=ShopItemType.AMULET, mpt=0., ppt=0.05)
        self.info = [f'+{self.ppt} ppt']


class Bakery(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Bakery', cost=Cost(1200., 0.1), type_=ShopItemType.BUSINESS, mpt=0.5, ppt=0)
        self.info = [f'+{self.mpt} mpt']


class BoostPpt(Effect):
    def __init__(self) -> None:
        super().__init__(name='Boost ppt', cost=Cost(900., 0.1), type_=ShopItemType.EFFECT, duration=30)
        self.info = ['ppt x 2  ->  pps x 1']

def create_shop() -> Shop:
    return Shop(
        [
            ShopCell(IronNugget()),
            ShopCell(CopperNugget()),
            ShopCell(Bakery()),
            ShopCell(BoostPpt())
        ]
    )
