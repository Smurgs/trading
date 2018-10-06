import os
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

import definitions
from DataModule.Data import Data
from DataModule.DataFrame import DataFrame
from Questrade import QuestradeWrapper

import requests


class DataManager(object):

    ALPHA_VANTAGE_URI = 'https://www.alphavantage.co/query'
    ALPHA_VANTAGE_API_KEY = '27E1IHARJVIL6KRU'
    ALPHA_VANTAGE_INTRADAY = 'TIME_SERIES_INTRADAY'
    ALPHA_VANTAGE_DAILY = 'TIME_SERIES_DAILY'

    def __init__(self):
        self.database_dir = definitions.DATABASE_DIR
        if not os.path.isdir(self.database_dir):
            raise NotADirectoryError('Database directory does not exist.')

    def get(self, symbol, start, end, interval):
        """Returns requested data. If not already in Database, it will be downloaded and saved for future use.

        Args:
            symbol (str): Stock symbol for requested data (ex. 'FB')
            start (datetime): Start of the request data sequence
            end (datetime): End of the request data sequence
            interval (Data.Interval): Enum, one of [ONE_MIN | FIVE_MIN | ONE_HOUR | ONE_DAY]

        Returns:
            Data: Requested data series
        """
        return self._load_data(symbol, start, end, interval)

    def download(self, symbol):
        """Download data minute and daily data to store in Database for future use.

            Args:
                symbol (str): Stock symbol for requested data (ex. 'FB')
        """
        # Get data
        day_data = self._download_data_alpha_vantage(symbol, Data.Interval.ONE_DAY)
        minute_data = self._download_data_alpha_vantage(symbol, Data.Interval.ONE_MIN)

        # Store data
        self._store_data(day_data)
        self._store_data(minute_data)

    @staticmethod
    def _download_data_questrade(symbol, start, end, interval):

        # Prepare request
        qt = QuestradeWrapper()
        qt.authenticate()
        qt_symbol = qt.search_symbol(symbol)
        qt_start = QuestradeWrapper.datetime_to_string(start)
        qt_end = QuestradeWrapper.datetime_to_string(end)
        if interval == Data.Interval.ONE_MIN:
            qt_interval = "OneMinute"
        elif interval == Data.Interval.ONE_DAY:
            qt_interval = "OneDay"
        else:
            raise ValueError("Download interval can only be one minute/day")

        # Get data
        qt_candles = qt.get_candles(qt_symbol, qt_start, qt_end, qt_interval)

        # Format into Data object
        data_frames = [DataFrame(QuestradeWrapper.string_to_datetime(x.start),
                                 QuestradeWrapper.string_to_datetime(x.end),
                                 x.open,
                                 x.high,
                                 x.low,
                                 x.close,
                                 x.volume) for x in qt_candles]
        data = Data(symbol, interval, data_frames)
        return Data.chop_unwanted_data(start, end, data)

    @staticmethod
    def _download_data_alpha_vantage(symbol, interval):

        # Prepare request
        params = {'symbol': symbol, 'outputsize': 'full', 'datatype': 'json',
                  'interval': Data.interval_to_string(interval), 'apikey': DataManager.ALPHA_VANTAGE_API_KEY}
        if interval == Data.Interval.ONE_DAY:
            params['function'] = DataManager.ALPHA_VANTAGE_DAILY
        elif interval == Data.Interval.ONE_MIN:
            params['function'] = DataManager.ALPHA_VANTAGE_INTRADAY
        else:
            raise ValueError("Download interval can only be one minute/day")

        # Download data
        response = requests.get(DataManager.ALPHA_VANTAGE_URI, params=params)
        response_json = response.json()
        data_json = response_json[list(response_json.keys())[1]]

        # Format into Data object
        data_frames = []
        if interval == Data.Interval.ONE_DAY:
            key_date_pairs = [(x, datetime.strptime(x, '%Y-%m-%d')) for x in data_json.keys()]
        else:
            key_date_pairs = [(x, datetime.strptime(x, '%Y-%m-%d %H:%M:%S')) for x in data_json.keys()]
        key_date_pairs = sorted(key_date_pairs, key=lambda x: x[1])
        for key, dt in key_date_pairs:
            data_frames.append(DataFrame(dt,
                                         dt + Data.interval_to_relativedate(interval),
                                         data_json[key]['1. open'],
                                         data_json[key]['2. high'],
                                         data_json[key]['3. low'],
                                         data_json[key]['4. close'],
                                         data_json[key]['5. volume']))

        # If last data frame is for today, its probably incomplete. Drop it.
        today = datetime.today()
        if data_frames[-1].start.year == today.year and data_frames[-1].start.month == today.month and data_frames[-1].start.day == today.day:
            data_frames = data_frames[:-1]

        return Data(symbol, interval, data_frames)

    def _build_file_path(self, symbol, year, month=None):
        file_path = os.path.join(self.database_dir, symbol)
        file_path = os.path.join(file_path, str(year))
        if month is not None:
            file_path = os.path.join(file_path, '%s_%d_%02d.json' % (symbol, year, month))
        else:
            file_path = os.path.join(file_path, '%s_%d.json' % (symbol, year))
        return file_path

    def _load_data(self, symbol, start, end, interval):
        data_frames = []
        file_path_lst = []
        iter = datetime(year=start.year, month=1 if interval == Data.Interval.ONE_DAY else start.month, day=1)
        inc = relativedelta(years=1) if interval == Data.Interval.ONE_DAY else relativedelta(months=1)
        while iter < end:
            file_path_lst.append(self._build_file_path(symbol, iter.year, None if interval == Data.Interval.ONE_DAY else iter.month))
            iter += inc

        for file_path in file_path_lst:
            if not os.path.isfile(file_path):
                raise FileNotFoundError('Could not load desired data for %s' % file_path)

            with open(file_path) as infile:
                data = Data.from_dict(json.load(infile))
            data_frames += data.data_frames
        data = Data(symbol, interval, data_frames)
        return Data.chop_unwanted_data(start, end, data)

    def _store_data(self, data):
        # Split into years (daily data) or months (minute data)
        years_dict = {year: [] for year in range(data.start.year, data.end.year+1)}
        for data_frame in data.data_frames:
            years_dict[data_frame.start.year].append(data_frame)

        # Save file path and data
        path_data_pairs = []
        for year in years_dict.keys():
            if data.interval == Data.Interval.ONE_DAY:
                year_data = Data(data.symbol, data.interval, years_dict[year])
                file_path = self._build_file_path(data.symbol, year)
                path_data_pairs.append((file_path, year_data))
            else:
                months_dict = {month: [] for month in range(years_dict[year][0].start.month, years_dict[year][-1].end.month+1)}
                for data_frame in years_dict[year]:
                    months_dict[data_frame.start.month].append(data_frame)

                for month in months_dict.keys():
                    month_data = Data(data.symbol, data.interval, months_dict[month])
                    file_path = self._build_file_path(data.symbol, year, month)
                    path_data_pairs.append((file_path, month_data))

        for file_path, file_data in path_data_pairs:
            # If file exists, re-write if there is new data
            if os.path.isfile(file_path):
                if data.interval == Data.Interval.ONE_DAY:
                    file_start = datetime(year=file_data.start.year, month=1, day=1)
                    file_end = datetime(year=file_data.start.year, month=12, day=31)
                else:
                    file_start = datetime(year=file_data.start.year, month=file_data.start.month, day=1)
                    file_end = datetime(year=file_data.start.year, month=file_data.start.month, day=file_data.data_frames[-1].start.day)
                existing_data = self._load_data(data.symbol, file_start, file_end, data.interval)
                if file_data.end == existing_data.end:
                    continue
                new_frames = [x for x in file_data.data_frames if x.start > existing_data.data_frames[-1].start]
                file_data = Data(data.symbol, data.interval, existing_data.data_frames + new_frames)
                os.remove(file_path)

            data_to_serialize = Data.to_dict(file_data)
            data_to_serialize['meta']['date_stored'] = datetime.today().strftime("%Y-%m-%d %H:%M")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w+') as outfile:
                json.dump(data_to_serialize, outfile)


if __name__ == '__main__':
    dm = DataManager()
    #dm.download('AAPL')
    start = datetime(year=2017, month=9, day=1)
    end = datetime(year=2017, month=10, day=1)
    data = dm.get('AAPL', start, end, Data.Interval.ONE_DAY)
    print('Symbol: %s' % data.symbol)
    print('Start: %s' % data.start)
    print('End: %s' % data.end)
    print('Interval: %s' % Data.interval_to_string(data.interval))
    print('Length: %d' % len(data.data_frames))
    print([DataFrame.to_dict(x) for x in data.data_frames])
