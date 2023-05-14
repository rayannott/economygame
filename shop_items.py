from base_objects import Cost, Shop, ShopCell, ShopItem, ProfitGen, ShopItemType, Effect


class IronNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Iron Nugget', cost=Cost(50., 0.1), type_=ShopItemType.AMULET, mpt=0., ppt=0.01)
        self.info = [f'+{self.ppt} ppt'] # a list of strings to display on ShopItemPanel


class CopperNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Copper Nugget', cost=Cost(600., 0.), type_=ShopItemType.AMULET, mpt=0., ppt=0.05)
        self.info = [f'+{self.ppt} ppt']


class GoldenNugget(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Golden Nugget', cost=Cost(1200., 0.1), type_=ShopItemType.AMULET, mpt=0.1, ppt=0.03)
        self.info = [f'+{self.mpt} mpt', f'+{self.ppt} ppt']


class Bakery(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Bakery', cost=Cost(400., 0.05), type_=ShopItemType.BUSINESS, mpt=0.3, ppt=0)
        self.info = [f'+{self.mpt} mpt']


class SouvenirShop(ProfitGen):
    def __init__(self) -> None:
        super().__init__(name='Souvenir Shop', cost=Cost(200., 0.2), type_=ShopItemType.BUSINESS, mpt=0.1, ppt=0)
        self.info = [f'+{self.mpt} x (# of amulets) mpt']


class BoostPpt(Effect):
    def __init__(self) -> None:
        super().__init__(name='Boost PPT', cost=Cost(100., 0.1), type_=ShopItemType.EFFECT, duration=30) # TODO: change cost
        self.info = ['2x(ppt) -> 1x(ppt)', f'in {self.duration} sec']


def create_shop() -> Shop:
    return Shop(
        [
            ShopCell(IronNugget()),
            ShopCell(CopperNugget()),
            ShopCell(GoldenNugget()),
            ShopCell(Bakery()),
            ShopCell(SouvenirShop()),
            ShopCell(BoostPpt())
        ]
    )
