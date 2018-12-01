from enum import Enum
from dateutil.relativedelta import relativedelta

from DataModule.DataFrame import DataFrame


class Data(object):

    class Interval(Enum):
        ONE_MIN = '1min'
        FIVE_MIN = '5min'
        TEN_MIN = '10min'
        FIFTEEN_MIN = '15min'
        THIRTY_MIN = '30min'
        ONE_DAY = '1day'

    def __init__(self, symbol, interval, data_frames):
        """Builds DataModule object that represents a data series for a single stock

            Args:
                symbol (str): ticker symbol
                interval (Data.Interval): interval between data points
                data_frames ([DataFrame]): list of data frames
        """
        self.symbol = symbol
        self.start = data_frames[0].start
        self.end = data_frames[-1].end
        self.interval = interval
        self.data_frames = data_frames

    @staticmethod
    def add_data_list(lst):
        lst = sorted(lst, key=lambda x: x.end.year)
        data_frames = []
        for l in lst:
            data_frames += l.data_frames
        data = Data(lst[0].symbol, lst[0].interval, data_frames)
        return data

    @staticmethod
    def to_dict(data):
        d = {'meta': {'symbol': data.symbol,
                      'year': data.end.year,
                      'interval': data.interval.value},
             'data': [DataFrame.to_dict(data_frame) for data_frame in data.data_frames]}
        return d

    @staticmethod
    def from_dict(json):
        symbol = json['meta']['symbol']
        interval = Data.string_to_interval(json['meta']['interval'])
        data_frames = [DataFrame.from_dict(x) for x in json['data']]
        data_frames = sorted(data_frames, key=lambda x: x.end)
        return Data(symbol, interval, data_frames)

    @staticmethod
    def string_to_interval(s):
        if s == '1min':
            return Data.Interval.ONE_MIN
        if s == '5min':
            return Data.Interval.FIVE_MIN
        if s == '10min':
            return Data.Interval.TEN_MIN
        if s == '15min':
            return Data.Interval.FIFTEEN_MIN
        if s == '30min':
            return Data.Interval.THIRTY_MIN
        if s == '1day':
            return Data.Interval.ONE_DAY

    @staticmethod
    def interval_to_relativedate(interval):
        """Returns string that corresponds to enum.

            Args:
                interval (Data.Interval): Enum, one of [ONE_MIN | FIVE_MIN | ONE_HOUR | ONE_DAY]

            Returns:
                relativedelta: Relative delta that corresponds to enum

            Raises:
                ValueError: If `interval` is not a valid DataModule.Interval enum
        """
        if interval == Data.Interval.ONE_MIN:
            return relativedelta(minutes=1)
        if interval == Data.Interval.FIVE_MIN:
            return relativedelta(minutes=5)
        if interval == Data.Interval.TEN_MIN:
            return relativedelta(minutes=10)
        if interval == Data.Interval.FIFTEEN_MIN:
            return relativedelta(minutes=15)
        if interval == Data.Interval.THIRTY_MIN:
            return relativedelta(minutes=30)
        if interval == Data.Interval.ONE_DAY:
            return relativedelta(days=1)
        raise ValueError("Provided interval is not a valid option")

    @staticmethod
    def chop_unwanted_data(start, end, data):
        start_index = 0
        end_index = len(data.data_frames) - 1
        while start > data.data_frames[start_index].start:
            start_index += 1
        while end < data.data_frames[end_index].end:
            end_index -= 1
        data.data_frames = data.data_frames[start_index:end_index+1]
        data.start = data.data_frames[0].start
        data.end = data.data_frames[-1].end
        return data
