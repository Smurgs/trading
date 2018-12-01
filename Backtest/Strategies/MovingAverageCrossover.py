from datetime import datetime

from DataModule.Data import Data
from Backtest.Action import Action
from DataModule.DataManager import DataManager
from Backtest.Strategies.Strategy import Strategy
from Backtest.Signals.MovingAverage import MovingAverage
from Backtest.Signals.RecentHigh import RecentHigh
from Backtest.Signals.RecentLow import RecentLow
from Backtest.Signals.Price import Price
from Backtest.Position import Position


class MovingAverageCrossover(Strategy):
    trade_open = False
    position = None
    entry_price = None

    def enter(self, signals):
        if signals['short_ma'] > signals['long_ma']:
            if signals['price'] >= signals['recent_high']:
                self.trade_open = True
                self.position = Position.LONG
                self.entry_price = signals['price']
                return Action('AAPL', Action.Operation.BUY, 1)

        elif signals['short_ma'] < signals['long_ma']:
            if signals['price'] <= signals['recent_low']:
                self.trade_open = True
                self.position = Position.SHORT
                self.entry_price = signals['price']
                return Action('AAPL', Action.Operation.SELL, 1)

        return None

    def exit(self, signals):
        if not self.trade_open:
            return False

        # Calculate draw down
        draw_down = self.position * (signals['price'] - self.entry_price) / self.entry_price
        if self.position == Position.SHORT:
            draw_down *= -1

        # Stop loss
        if draw_down < -0.05:
            return True

        return False

    def get_data(self):
        data_manger = DataManager()
        start = datetime(2017, 10, 31)
        end = datetime(2018, 10, 31)
        return data_manger.get('AAPL', Data.Interval.THIRTY_MIN, start, end)

    def get_signals(self):
        signals = {
            'short_ma': MovingAverage(3),
            'long_ma': MovingAverage(20),
            'recent_high': RecentHigh(3),
            'recent_low': RecentLow(3),
            'price': Price()
        }
        return signals
