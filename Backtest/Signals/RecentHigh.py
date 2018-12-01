from Backtest.Signals.Signal import Signal


class RecentHigh(Signal):

    def __init__(self, window_size):
        self.window_size = window_size

    def get_min_data_points(self):
        return self.window_size

    def calculate(self, data_frames):
        self._verify_size(data_frames)
        return max([x.close for x in data_frames])
