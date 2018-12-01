import json
import time
import logging
from datetime import datetime

from definitions import *
from Backtest.Simulator import Simulator
from Backtest.Strategies.FollowMovingAverageSlope import FollowMovingAverageSlope
from DataModule.DataManager import DataManager
from DataModule.Data import Data


class Optimizer(object):

    def __init__(self, strategy, output_filename, data):
        self.strategy = strategy
        self.output_path = os.path.join(ROOT_DIR, 'logs')
        self.output_path = os.path.join(self.output_path, output_filename)
        if os.path.isfile(self.output_path):
            raise ValueError('File already exists with name: %s' % output_filename)
        self.param_value_sets = [[]]
        self.param_names = []
        self.param_values = []
        self.data = data

    def add_param(self, name, start_value, end_value=None, interval=None):
        # Generate values for added param
        new_param_values = []
        if interval == 0 or end_value is None or interval is None:
            new_param_values.append([start_value])
        else:
            value_iter = start_value
            while value_iter <= end_value:
                new_param_values.append(value_iter)
                value_iter += interval

        # Create all combinations of values for all params
        new_value_sets = []
        for param_value in new_param_values:
            for value_set in self.param_value_sets:
                new_value_sets.append(value_set + [param_value])

        # Save param name and all generated value sets
        self.param_value_sets = new_value_sets
        self.param_names.append(name)
        self.param_values.append(new_param_values)

    def run(self):
        simulation_results = []
        logger = logging.getLogger()
        for param_value_set in self.param_value_sets:

            # Build param dict
            param_dict = self._build_param_dict(param_value_set)
            logger.info('Running strategy withe params: ' + str(param_dict))

            # Run simulation
            strategy = self.strategy(**param_dict)
            simulator = Simulator(strategy, self.data, headless=True)
            simulator.run()

            # Record result
            result = simulator.trade_log.stats
            simulation_results.append({'params': param_dict, 'stats': result})
            net_profit = result['all']['net_profit']
            logger.info('Net profit for strategy: ' + str(net_profit))

        logger.info('Finished running strategies')

        # Log largest net profit
        max_param = simulation_results[0]['params']
        max_stats = simulation_results[0]['stats']
        for result in simulation_results:
            param = result['params']
            stats = result['stats']
            if stats['all']['net_profit'] > max_stats['all']['net_profit']:
                max_param = param
                max_stats = stats
        logger.info('Maximum net profit was ' + str(max_stats['all']['net_profit']) + ' with params: ' + str(max_param))

        # Save results to file
        param_ranges = {}
        for i in range(len(self.param_names)):
            param_ranges[self.param_names[i]] = self.param_values[i]
        outdata = {
            'meta': {
                'strategy': self.strategy().__class__.__name__,
                'symbol': self.data.symbol,
                'interval': self.data.interval.value,
                'start': self.data.start.strftime("%Y-%m-%d %H:%M"),
                'end': self.data.end.strftime("%Y-%m-%d %H:%M"),
                'params': param_ranges
            },
            'results': simulation_results
        }
        with open(self.output_path, 'w+') as outfile:
            json.dump(outdata, outfile, separators=(',', ':'), indent=2)
        logger.info('Saved results to log file: ' + self.output_path)

    def _build_param_dict(self, param_value_set):
        param_dict = {}
        for i in range(len(self.param_names)):
            param_dict[self.param_names[i]] = param_value_set[i]
        return param_dict


if __name__ == '__main__':
    start = time.time()

    # Setup logger
    fmt = '%(asctime)s - [%(levelname)s] - %(message)s'
    datefmt = '%d-%b-%y %H:%M:%S'
    log_file = os.path.join(ROOT_DIR, 'logs/optimizer_log.txt')
    logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO, filename=log_file)
    logging.getLogger().addHandler(logging.StreamHandler())

    # Prepare data
    data_manger = DataManager()
    data_start = datetime(2017, 10, 31)
    data_end = datetime(2018, 10, 31)
    data = data_manger.get('AAPL', Data.Interval.THIRTY_MIN, data_start)

    optimizer = Optimizer(FollowMovingAverageSlope, 'followMovingAvgSlope_AAPL_30min.json', data)
    optimizer.add_param('abs_slope', 0, 0.02, 0.005)
    optimizer.add_param('stop_loss', 0, 0.05, 0.01)
    optimizer.add_param('ma_slope', 10, 100, 10)
    optimizer.run()

    end = time.time()
    logger = logging.getLogger()
    logger.info('Run time: ' + str(end - start))



