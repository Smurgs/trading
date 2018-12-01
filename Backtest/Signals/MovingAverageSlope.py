from Backtest.Signals.Signal import Signal


class MovingAverageSlope(Signal):
    last_ma = None

    def __init__(self, window_size):
        if window_size <= 1:
            raise ValueError('Window size should be larger than 1 for MovingAverageSlope')
        self.window_size = window_size

    def get_min_data_points(self):
        return self.window_size

    def calculate(self, data_frames):
        self._verify_size(data_frames)
        new_ma = sum([float(x.close) for x in data_frames]) / self.window_size
        if self.last_ma is None:
            last_ma = sum([float(x.close) for x in data_frames[:-1]]) / self.window_size-1
            slope = new_ma - last_ma
        else:
            slope = new_ma - self.last_ma
        self.last_ma = new_ma
        return slope
