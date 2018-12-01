from datetime import datetime

from DataModule.Data import Data
from Backtest.Action import Action
from DataModule.DataManager import DataManager
from Backtest.Strategies.Strategy import Strategy
from Backtest.Signals.MovingAverageSlope import MovingAverageSlope
from Backtest.Signals.HourSignal import HourSignal
from Backtest.Signals.MinuteSignal import MinuteSignal
from Backtest.Signals.Price import Price
from Backtest.Position import Position
from Backtest.Signals.DayOfWeekSignal import DayOfWeekSignal

abs_slope = 0.0


class BuyHoldForever(Strategy):

    trade_open = False

    def enter(self, signals):
        if self.trade_open:
            return None

        return Action('AAPL', Action.Operation.BUY, 1)

    def exit(self, signals):
        return False

    def get_data(self):
        data_manger = DataManager()
        start = datetime(2010, 10, 31)
        end = datetime(2018, 10, 31)
        return data_manger.get('AAPL', Data.Interval.THIRTY_MIN, start, end)

    def get_signals(self):
        signals = {
            'price': Price()
        }
        return signals
