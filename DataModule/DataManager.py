import os
import json
import time
import logging
import shutil
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

    def __init__(self, database_dir=definitions.DATABASE_DIR):
        self.database_dir = database_dir
        if not os.path.isdir(self.database_dir):
            raise NotADirectoryError('Database directory does not exist: %s' % self.database_dir)

    def get(self, symbol, interval, start, end=None):
        """Returns requested data. If not already in Database, it will be downloaded and saved for future use.

        Args:
            symbol (str): Stock symbol for requested data (ex. 'FB')
            start (datetime): Start of the request data sequence
            end (datetime): End of the request data sequence
            interval (Data.Interval): Enum, one of [ONE_MIN | FIVE_MIN | ONE_HOUR | ONE_DAY]

        Returns:
            Data: Requested data series
        """
        today = datetime.today()
        if end is None:
            end = today

        # Validate object types
        if type(start) != datetime or type(end) != datetime:
            raise AssertionError('Parameters `start` and `end` must be a datetime object')
        if type(interval) != Data.Interval:
            raise AssertionError('Parameter `interval` must be a DataManger.Data.Interval enum')

        # Validate request start and end values
        if start > end:
            raise ValueError('Paramerter `start` cannot be larger than parameter `end`')
        if start > today or end > today:
            raise ValueError('Paramerters `start` and `end` cannot be in the future')

        # Ensure symbol is all upper case
        symbol = symbol.upper()

        # Only use year/month/day from dates, drop additional info
        start = datetime(start.year, start.month, start.day)
        end = datetime(end.year, end.month, end.day)

        # Trim weekends off start and end dates
        while start.weekday() > 4:
            start += relativedelta(days=1)
        while end.weekday() > 4:
            end -= relativedelta(days=1)

        load_interval = Data.Interval.ONE_DAY if interval == Data.Interval.ONE_DAY else Data.Interval.ONE_MIN
        try:
            loaded_data = self._load_data(symbol, load_interval, start, end)
        except FileNotFoundError:
            raise ValueError('Database does not have all the data queried for')

        # Change 1min interval to 5/10/15/30min if need be
        if load_interval != interval:
            loaded_data = self._rebuild_interval(loaded_data, interval)

        # Remove pre/post market data
        loaded_data = self._remove_pre_post(loaded_data)

        return loaded_data

    def download(self, symbol):
        """Download data minute data to store in Database for future use.

            Args:
                symbol (str): Stock symbol for requested data (ex. 'FB')
        """
        today = datetime.today()
        end_date = datetime(today.year, today.month, today.day)
        start_date = end_date - relativedelta(days=20)
        minute_data = self._download_data_questrade(symbol, Data.Interval.ONE_MIN, start_date, end_date)
        if minute_data is None:
            return None

        # Store data
        self._store_data(minute_data)

    @staticmethod
    def _download_data_questrade(symbol, interval, start_date, end_date):

        # Prepare request
        qt = QuestradeWrapper()
        qt.authenticate()
        qt_symbol = qt.search_symbol(symbol)
        qt_start = QuestradeWrapper.datetime_to_string(start_date)
        qt_end = QuestradeWrapper.datetime_to_string(end_date)
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
        return Data.chop_unwanted_data(start_date, end_date, data)

    @staticmethod
    def _download_data_alpha_vantage(symbol, interval):
        LOGGER = logging.getLogger()

        # Prepare request
        params = {'symbol': symbol, 'outputsize': 'full', 'datatype': 'json',
                  'interval': interval.value, 'apikey': DataManager.ALPHA_VANTAGE_API_KEY}
        if interval == Data.Interval.ONE_DAY:
            params['function'] = DataManager.ALPHA_VANTAGE_DAILY
        elif interval == Data.Interval.ONE_MIN:
            params['function'] = DataManager.ALPHA_VANTAGE_INTRADAY
        else:
            raise ValueError("Download interval can only be one minute/day")

        retries = 5
        delay = 30
        while True:
            try:
                # Download data
                response = requests.get(DataManager.ALPHA_VANTAGE_URI, params=params)
                response_json = response.json()

                # API error
                if 'Error Message' in response_json.keys():
                    LOGGER.error('Received error from API for symbol %s: %s' % (symbol, response_json['Error Message']))
                    return None

                # If we hit API limit, retry in 65s
                if 'Information' in response_json.keys():
                    LOGGER.warning('Probably hit API limit, trying again in %ds' % delay)

                # If fail to find time series data in response, try again in 20s
                time_series_key = [key for key in response_json.keys() if 'Time Series' in key]
                if len(time_series_key) < 1:
                    LOGGER.warning('Failed to find time series in response, trying again in %ds' % delay)
                else:
                    break
            except:
                LOGGER.warning('Unexpected error while querying API for symbol %s, trying again in %ds' % (symbol, delay))

            retries -= 1
            if retries == 0:
                LOGGER.error('Failed to query API for symbol %s after multiple attempts' % symbol)
                return None
            time.sleep(delay)

        # Format into Data object
        data_json = response_json[time_series_key[0]]
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

    def build_file_path(self, symbol, year, month=None):
        file_path = os.path.join(self.database_dir, symbol)
        file_path = os.path.join(file_path, str(year))
        if month is not None:
            file_path = os.path.join(file_path, '%s_%d_%02d.json' % (symbol, year, month))
        else:
            file_path = os.path.join(file_path, '%s_%d.json' % (symbol, year))
        return file_path

    def _load_data(self, symbol, interval, start, end):
        data_frames = []
        file_path_lst = []
        iterator = datetime(year=start.year, month=1 if interval == Data.Interval.ONE_DAY else start.month, day=1)
        increment = relativedelta(years=1) if interval == Data.Interval.ONE_DAY else relativedelta(months=1)
        while iterator < end:
            file_path_lst.append(self.build_file_path(symbol, iterator.year, None if interval == Data.Interval.ONE_DAY else iterator.month))
            iterator += increment

        for file_path in file_path_lst:
            file_data = self._load_file(file_path)
            data_frames += file_data.data_frames
        loaded_data = Data(symbol, interval, data_frames)
        return Data.chop_unwanted_data(start, end, loaded_data)

    @staticmethod
    def _load_file(file_path):
        if not os.path.isfile(file_path):
            raise FileNotFoundError('Could not load desired data for %s' % file_path)
        with open(file_path) as infile:
            file_data = Data.from_dict(json.load(infile))
        return file_data

    def _store_data(self, data):
        # Split into years (daily data) or months (minute data)
        years_dict = {year: [] for year in range(data.start.year, data.end.year+1)}
        for data_frame in data.data_frames:
            years_dict[data_frame.start.year].append(data_frame)

        # Save file path and data
        path_data_pairs = []
        for year in years_dict.keys():
            if len(years_dict[year]) == 0:
                continue
            if data.interval == Data.Interval.ONE_DAY:
                year_data = Data(data.symbol, data.interval, years_dict[year])
                file_path = self.build_file_path(data.symbol, year)
                path_data_pairs.append((file_path, year_data))
            else:
                months_dict = {month: [] for month in range(years_dict[year][0].start.month, years_dict[year][-1].end.month+1)}
                for data_frame in years_dict[year]:
                    months_dict[data_frame.start.month].append(data_frame)

                for month in months_dict.keys():
                    month_data = Data(data.symbol, data.interval, months_dict[month])
                    file_path = self.build_file_path(data.symbol, year, month)
                    path_data_pairs.append((file_path, month_data))

        for file_path, file_data in path_data_pairs:
            self._store_file(file_path, file_data)

    @staticmethod
    def _store_file(file_path, file_data):
        backup_suffix = '.backup'

        # If file exists (usually the case), re-write if there is new data
        if os.path.isfile(file_path):

            # Check if backup also exists (only when previous store was interrupted)
            if os.path.isfile(file_path + backup_suffix):

                # If old target is largest, remove backup
                if os.path.getsize(file_path) >= os.path.getsize(file_path + backup_suffix):
                    os.remove(file_path + backup_suffix)

                # Else backup is largest, copy to target and remove backup
                else:
                    shutil.copyfile(file_path + backup_suffix, file_path)
                    os.remove(file_path + backup_suffix)

            # Copy old target to backup
            shutil.copyfile(file_path, file_path + backup_suffix)

            # Get old data
            existing_data = DataManager._load_file(file_path)
            new_frames = [x for x in file_data.data_frames if x.start > existing_data.data_frames[-1].start]
            file_data = Data(existing_data.symbol, existing_data.interval, existing_data.data_frames + new_frames)

            # Delete old target
            os.remove(file_path)

        # Write new target
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        data_to_serialize = Data.to_dict(file_data)
        data_to_serialize['meta']['date_stored'] = datetime.today().strftime("%Y-%m-%d %H:%M")
        with open(file_path, 'w+') as outfile:
            json.dump(data_to_serialize, outfile, separators=(',', ':'), indent=2)

        # Delete backup (if exists)
        if os.path.isfile(file_path + backup_suffix):
            os.remove(file_path + backup_suffix)

    @staticmethod
    def _remove_pre_post(data):
        target_data_frames = []
        for data_frame in data.data_frames:
            # Don't include pre-market
            if data_frame.start.hour < 9:
                continue
            elif data_frame.start.hour == 9 and data_frame.start.minute < 30:
                continue

            # Don't include post-market
            if data_frame.end.hour > 16:
                continue
            elif data_frame.end.hour == 4 and data_frame.end.minute > 0:
                continue

            target_data_frames.append(data_frame)

        return Data(data.symbol, data.interval, target_data_frames)

    @staticmethod
    def _rebuild_interval(data, target_interval):

        # Create list of upper bounds
        relative_date = Data.interval_to_relativedate(target_interval)
        upper_time_bound = datetime(1899, 1, 1, 9, 30)
        upper_bounds = []
        while upper_time_bound < datetime(1899, 1, 1, 16, 0):
            upper_bounds.append(upper_time_bound + relative_date)
            upper_time_bound += relative_date

        # Loop through data frames
        bound_iter = 0
        target_data_frames = []
        packet = []
        upper_bound = upper_bounds[-1]
        for data_frame in data.data_frames:

            if data_frame.start.hour >= 16:
                continue

            if data_frame.end > upper_bound:
                # Build packet thats ready to be built
                if len(packet) > 0:
                    packet_data_frame = DataFrame.combine_frames(packet)
                    target_data_frames.append(packet_data_frame)
                    packet = []

                # Increase upper bound
                while data_frame.end > upper_bound:
                    upper_bound = datetime(data_frame.end.year, data_frame.end.month, data_frame.end.day,
                                           upper_bounds[bound_iter].hour, upper_bounds[bound_iter].minute)
                    bound_iter += 1
                    if bound_iter == len(upper_bounds):
                        bound_iter = 0

            # Add frame to packet to be built
            packet.append(data_frame)

        return Data(data.symbol, target_interval, target_data_frames)


if __name__ == '__main__':
    dm = DataManager('/localdisk/trading')
    start = datetime(year=2018, month=10, day=20)
    end = datetime(year=2018, month=11, day=7)
    data = dm._download_data_questrade('PG', Data.Interval.ONE_MIN, start, end)
    print('Symbol: %s' % data.symbol)
    print('Start: %s' % data.start)
    print('End: %s' % data.end)
    print('Interval: %s' % data.interval)
    print('Length: %d' % len(data.data_frames))

