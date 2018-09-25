from datetime import datetime
from dateutil.relativedelta import relativedelta

from definitions import *
from Questrade import QuestradeWrapper, Symbol

import numpy as np
from pandas.tseries.holiday import USFederalHolidayCalendar as FedHoliday


class SimpleModelDataSetBuilder(object):

    def __init__(self, symbols=('FB', 'AAPL', 'AMZN', 'NFLX', 'GOOG', 'AMD', 'MU', 'SNAP', 'MSFT', 'NVDA')):
        self.window_size = 250
        self.data_points_per_stock = 300
        self.threshold = 0.0025
        self.dataset_name = 'simple_model_dataset'

        self.end_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        self.symbols = [symbol.upper() for symbol in symbols]
        self.dataset_path = os.path.join(DATASET_DIR, self.dataset_name + '.npz')

    def iso(self, dt):
        return '%d-%02d-%02dT%02d:%02d:00-04:00' % (dt.year, dt.month, dt.day, dt.hour, dt.minute)

    def dt(self, iso):
        return datetime.strptime(iso[:-13], '%Y-%m-%dT%H:%M:%S')

    def prepare_dataset(self):
        LOGGER = logging.getLogger()

        LOGGER.info('Checking if dataset already exists')
        if os.path.isfile(self.dataset_path):
            LOGGER.info('Dataset found')
            return self.dataset_path

        LOGGER.info('Building dataset')

        LOGGER.info('Authenticating with Questrade')
        qt = QuestradeWrapper()
        qt.authenticate()

        LOGGER.info('Getting symbol IDs from Questrade')
        symbol_ids = [Symbol(qt.search_symbol(symbol)) for symbol in self.symbols]

        LOGGER.info('Downloading data from Questrade')
        data_lst = {x.symbolId: {'min': [], 'hour': [], 'day': []} for x in symbol_ids}
        data_map = {x.symbolId: {'min': {}, 'hour': {}, 'day': {}} for x in symbol_ids}
        min_start = self.end_date - relativedelta(months=1)
        hour_start = self.end_date - relativedelta(months=4)
        day_start = self.end_date - relativedelta(years=2)
        for sym_id in symbol_ids:
            data_lst[sym_id.symbolId]['min'] = qt.get_candles(sym_id, self.iso(min_start), self.iso(self.end_date), 'OneMinute')
            data_lst[sym_id.symbolId]['hour'] = qt.get_candles(sym_id, self.iso(hour_start), self.iso(self.end_date), 'OneHour')
            data_lst[sym_id.symbolId]['day'] = qt.get_candles(sym_id, self.iso(day_start), self.iso(self.end_date), 'OneDay')

        LOGGER.info('Converting datetime')
        for sym_id in symbol_ids:
            for candle in data_lst[sym_id.symbolId]['min']:
                candle.end = self.dt(candle.end)
            for candle in data_lst[sym_id.symbolId]['hour']:
                candle.end = self.dt(candle.end)
            for candle in data_lst[sym_id.symbolId]['day']:
                candle.end = self.dt(candle.end)

        LOGGER.info('Inserting data into map')
        for sym_id in symbol_ids:
            for candle in data_lst[sym_id.symbolId]['min']:
                if candle.end.minute == 0 or candle.end.minute == 15 or candle.end.minute == 30 or candle.end.minute == 45:
                    data_map[sym_id.symbolId]['min'][candle.end] = data_lst[sym_id.symbolId]['min'].index(candle)
            for candle in data_lst[sym_id.symbolId]['hour']:
                data_map[sym_id.symbolId]['hour'][candle.end] = data_lst[sym_id.symbolId]['hour'].index(candle)
            for candle in data_lst[sym_id.symbolId]['day']:
                data_map[sym_id.symbolId]['day'][candle.end] = data_lst[sym_id.symbolId]['day'].index(candle)

        # Prepare some stuff for the upcoming loop
        x = np.zeros((self.data_points_per_stock * len(symbol_ids), self.window_size, 12), dtype=np.float32)
        y = np.zeros((self.data_points_per_stock * len(symbol_ids), 1), dtype=np.int32)
        hour_minute_samples = [(9, 30), (9, 45), (15, 0)] + [(x,y) for x in range(10, 14+1) for y in range(0, 45+1, 15)]
        hour_minute_samples.sort(reverse=True)
        us_holidays = FedHoliday().holidays(self.end_date - relativedelta(years=3), self.end_date).to_pydatetime()

        LOGGER.info('Forming training data')
        matrix_index = 0
        date_iterator = self.end_date
        while True:
            date_iterator = date_iterator - relativedelta(days=1)

            # Skip weekends and holidays
            if date_iterator.weekday() >= 5 or date_iterator in us_holidays:
                continue

            # 15-minute intervals -> 9:30, 9:45, 10:00, 10:15, ..., 14:30, 14:45, 15:00
            for hour, minute in hour_minute_samples:
                end_datetime = date_iterator.replace(hour=hour, minute=minute)

                for sym_id in symbol_ids:

                    try:
                        min_end_index = data_map[sym_id.symbolId]['min'][end_datetime]
                        min_start_index = min_end_index - self.window_size
                        hour_end_index = data_map[sym_id.symbolId]['hour'][end_datetime.replace(minute=0)]
                        hour_start_index = hour_end_index - self.window_size
                        day_end_index = data_map[sym_id.symbolId]['day'][end_datetime.replace(hour=0, minute=0)]
                        day_start_index = day_end_index - self.window_size
                    except KeyError:
                        continue

                    min_data = data_lst[sym_id.symbolId]['min'][min_start_index:min_end_index]
                    hour_data = data_lst[sym_id.symbolId]['hour'][hour_start_index:hour_end_index]
                    day_data = data_lst[sym_id.symbolId]['day'][day_start_index:day_end_index]

                    # Insert training data into x matrix
                    for i in range(len(min_data)):
                        for data, index in ((min_data, 0), (hour_data, 1), (day_data, 2)):
                            x[matrix_index][i][(index * 4) + 0] = data[i].close
                            x[matrix_index][i][(index * 4) + 1] = data[i].volume
                            x[matrix_index][i][(index * 4) + 2] = ((16 - data[i].end.hour) * 60) + 60 - data[i].end.minute
                            x[matrix_index][i][(index * 4) + 3] = data[i].end.weekday()

                    # Insert label data into y vector
                    label_data = [data_lst[sym_id.symbolId]['min'][x] for x in range(min_end_index, min_end_index+61, 60)]
                    hour_change = (label_data[1].close - label_data[0].close) / label_data[0].close
                    y[matrix_index] = 0 if hour_change < (-self.threshold) else 2 if hour_change > self.threshold else 1

                    matrix_index += 1
                    LOGGER.info('Collected %d data points' % matrix_index)

                    if matrix_index >= self.data_points_per_stock * len(symbol_ids): break
                if matrix_index >= self.data_points_per_stock * len(symbol_ids): break
            if matrix_index >= self.data_points_per_stock * len(symbol_ids): break

        LOGGER.info('Saving dataset')
        np.savez(self.dataset_path, x=x, y=y)

        LOGGER.info('Dataset is ready')
        return self.dataset_path


if __name__ == '__main__':
    simple_model_dataset_builder = SimpleModelDataSetBuilder()
    simple_model_dataset_builder.prepare_dataset()
