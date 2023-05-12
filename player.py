import math

from utils import INITIAL_BALANCE, INITIAL_MPT, INITIAL_PPT, GOAL_BALANCE


class Player:
    def __init__(self) -> None:
        self.balance = INITIAL_BALANCE
        self.mpt = INITIAL_MPT
        self.ppt = INITIAL_PPT
    
    def tick(self):
        self.balance *= 1+self.ppt*0.01
        self.balance += self.mpt

    def time_until_victory(self) -> float:
        return math.log((GOAL_BALANCE + 100*self.mpt/(self.ppt))/(self.balance + 100*self.mpt/(self.ppt)), 1+self.ppt*0.01)
