from datetime import datetime


class DataFrame(object):
    def __init__(self, start, end, open, high, low, close, volume):
        """Builds DataFrame object that represents a stock price for an interval of time

            Args:
                start (datetime): start time of interval for data point
                end (datetime): end time of interval for data point
                open (float): open price for interval
                high (float): highest price during interval
                low (float): lowest price during interval
                close (float): closing price for interval
                volume (int): volume traded during interval
        """
        self.start = start
        self.end = end
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume

    @staticmethod
    def to_dict(df):
        if type(df) is not DataFrame:
            raise ValueError('Function only accepts DataFrame objects')

        ret = {
            'start': df.start.strftime("%Y-%m-%d %H:%M"),
            'end': df.end.strftime("%Y-%m-%d %H:%M"),
            'open': df.open,
            'high': df.high,
            'low': df.low,
            'close': df.close,
            'volume': df.volume
        }
        return ret

    @staticmethod
    def from_dict(json):
        start = datetime.strptime(json['start'], '%Y-%m-%d %H:%M')
        end = datetime.strptime(json['end'], '%Y-%m-%d %H:%M')
        open = json['open']
        high = json['high']
        low = json['low']
        close = json['close']
        volume = json['volume']
        return DataFrame(start, end, open, high, low, close, volume)

    @staticmethod
    def combine_frames(data_frames):
        data_frames = sorted(data_frames, key=lambda x: x.start)
        start = data_frames[0].start
        end = data_frames[-1].end
        open = data_frames[0].open
        close = data_frames[-1].close
        volume = sum([int(x.volume) for x in data_frames])
        high = sum([float(x.high) for x in data_frames])
        low = sum([float(x.low) for x in data_frames])
        return DataFrame(start, end, open, high, low, close, volume)
