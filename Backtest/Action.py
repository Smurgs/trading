from enum import Enum


class Action(object):

    class Operation(Enum):
        BUY = 0
        SELL = 1

    def __init__(self, symbol, op, quantity):
        self.symbol = symbol
        self.op = op
        self.quantity = quantity
