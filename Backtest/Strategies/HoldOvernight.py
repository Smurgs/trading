from datetime import datetime

from DataModule.Data import Data
from Backtest.Action import Action
from DataModule.DataManager import DataManager
from Backtest.Strategies.Strategy import Strategy
from Backtest.Signals.MovingAverageSlope import MovingAverageSlope
from Backtest.Signals.HourSignal import HourSignal
from Backtest.Signals.MinuteSignal import MinuteSignal
from Backtest.Signals.Price import Price
from Backtest.Signals.DayOfWeekSignal import DayOfWeekSignal

abs_slope = 0.0


class HoldOvernight(Strategy):
    trade_open = False

    def enter(self, signals):
        if signals['hour'] == 16 and signals['min'] == 0:
            if signals['ma_slope'] > abs_slope:
                self.trade_open = True
                return Action('AAPL', Action.Operation.BUY, 1)

            elif signals['ma_slope'] < -1*abs_slope:
                self.trade_open = True
                return Action('AAPL', Action.Operation.SELL, 1)

        return None

    def exit(self, signals):
        if not self.trade_open:
            return False

        # Exit at 10am
        if signals['hour'] == 10 and signals['min'] == 0:
            return True

        return False

    def get_data(self):
        data_manger = DataManager()
        start = datetime(2010, 10, 31)
        end = datetime(2018, 10, 31)
        return data_manger.get('AAPL', Data.Interval.THIRTY_MIN, start, end)

    def get_signals(self):
        signals = {
            'ma_slope': MovingAverageSlope(50),
            'price': Price(),
            'hour': HourSignal(),
            'min': MinuteSignal(),
            'day': DayOfWeekSignal()
        }
        return signals
