from datetime import datetime

from DataModule.OptionDataFrame import OptionDataFrame


class OptionData(object):

    def __init__(self, symbol, expiry, strike, option_type, frames):
        """Builds OptionDataModule object that represents an option data series for a single stock, strike and expiry

            Args:
                symbol (str): ticker symbol
                expiry (datetime): expiry date of the contract
                type (str): either 'C' or 'P' for call or put
                frames ([OptionDataFrame]): list of option data frames
        """
        self.symbol = symbol
        self.expiry = expiry
        self.strike = strike
        self.option_type = option_type
        self.start = frames[0].time
        self.end = frames[-1].time
        self.frames = frames

    @staticmethod
    def to_dict(data):
        d = {'meta': {'symbol': data.symbol,
                      'expiry': data.expiry.strftime("%Y-%m-%d %H:%M"),
                      'strike': data.strike,
                      'optionType': data.option_type,
                      'interval': '5min'
                      },
             'data': [OptionDataFrame.to_dict(frame) for frame in data.frames]}
        return d

    @staticmethod
    def from_dict(json):
        symbol = json['meta']['symbol']
        expiry = datetime.strptime(json['meta']['expiry'], '%Y-%m-%d %H:%M')
        strike = json['meta']['strike']
        option_type = json['meta']['optionType']

        frames = [OptionDataFrame.from_dict(x) for x in json['data']]
        frames = sorted(frames, key=lambda x: x.time)
        return OptionData(symbol, expiry, strike, option_type, frames)
