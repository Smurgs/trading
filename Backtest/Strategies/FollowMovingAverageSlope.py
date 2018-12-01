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


class FollowMovingAverageSlope(Strategy):

    def __init__(self, abs_slope=0, stop_loss=0.02, ma_slope=50):
        self.abs_slope = abs_slope
        self.stop_loss = stop_loss
        self.ma_slope = ma_slope
        self.trade_open = False
        self.position = None
        self.entry_price = None
        self.max_gain = None

    def enter(self, signals):
        if self.trade_open:
            return None

        if signals['ma_slope'] > self.abs_slope and self.position != Position.LONG:
            self.trade_open = True
            self.position = Position.LONG
            self.entry_price = signals['price']
            self.max_gain = 0
            return Action('AAPL', Action.Operation.BUY, 1)

        elif signals['ma_slope'] < -1*self.abs_slope and self.position != Position.SHORT:
            self.trade_open = True
            self.position = Position.SHORT
            self.entry_price = signals['price']
            self.max_gain = 0
            return Action('AAPL', Action.Operation.SELL, 1)

        return None

    def exit(self, signals):
        if not self.trade_open:
            return False

        if signals['ma_slope'] < self.abs_slope and self.position == Position.LONG:
            self.trade_open = False
            self.position = None
            return True

        elif signals['ma_slope'] > -1*self.abs_slope and self.position == Position.SHORT:
            self.trade_open = False
            self.position = None
            return True

        gain = signals['price'] - self.entry_price
        if self.position == Position.SHORT:
            gain *= -1
        draw_down = gain / self.entry_price
        if draw_down < -1*self.stop_loss:
            return True

        return False

    def get_data(self):
        data_manger = DataManager()
        start = datetime(2010, 10, 31)
        end = datetime(2018, 10, 31)
        return data_manger.get('AAPL', Data.Interval.THIRTY_MIN, start, end)

    def get_signals(self):
        signals = {
            'ma_slope': MovingAverageSlope(self.ma_slope),
            'price': Price(),
            'hour': HourSignal(),
            'min': MinuteSignal(),
            'day': DayOfWeekSignal()
        }
        return signals
