from Backtest.Signals.Signal import Signal


class DayOfWeekSignal(Signal):

    def get_min_data_points(self):
        return 1

    def calculate(self, data_frames):
        self._verify_size(data_frames)
        return data_frames[0].end.weekday()
