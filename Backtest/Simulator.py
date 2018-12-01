from Backtest.TradeLog import TradeLog


class Simulator(object):

    def __init__(self, strategy, data=None, headless=False):
        self.strategy = strategy
        self.data = data if data is not None else strategy.get_data()
        self.headless = headless
        self.signals = strategy.get_signals()
        self.trade_log = TradeLog(self.data)
        self.data_iterator = 0
        self.position = None

    def run(self):

        # Traverse data by min required by all signals
        self.data_iterator = max([self.signals[x].get_min_data_points() for x in self.signals])
        if len(self.data.data_frames) <= self.data_iterator:
            raise ValueError('Not enough data points to simulate anything')

        # Simulation loop
        while True:

            # Calculate signals
            calculated_signals = self._calculate_signals()

            # Call strategy enter
            action = self.strategy.enter(calculated_signals)
            if action is not None and action.op != self.position:
                self.trade_log.close_position(self.data_iterator, self.data.data_frames[self.data_iterator])
                self.trade_log.execute_action(self.data_iterator, self.data.data_frames[self.data_iterator], action)
                self.position = action.op

            else:
                if self.strategy.exit(calculated_signals):
                    self.trade_log.close_position(self.data_iterator, self.data.data_frames[self.data_iterator])
                    self.position = None

            # Increment iterator, exit if at end of data
            self.data_iterator += 1
            if self.data_iterator >= len(self.data.data_frames)-1:
                break

        # Close any open positions and compile report
        self.trade_log.close_position(self.data_iterator, self.data.data_frames[self.data_iterator])
        self.trade_log.simulation_complete()
        if not self.headless:
            self.trade_log.print_stats()
            self.trade_log.plot_graphs()

    def _calculate_signals(self):
        signals = self.signals.copy()
        for key in signals:
            start_index = self.data_iterator - signals[key].get_min_data_points()
            end_index = self.data_iterator
            signals[key] = signals[key].calculate(self.data.data_frames[start_index:end_index])
        return signals
