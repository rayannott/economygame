from utils import INITIAL_BALANCE, INITIAL_MPS, INITIAL_PPS


class Player:
    def __init__(self) -> None:
        self.balance = INITIAL_BALANCE
        self.mps = INITIAL_MPS
        self.pps = INITIAL_PPS
    
    def tick(self):
        ...

