from Questrade import utils


class Candle(object):

    def __init__(self, candle_dict):
        self.start = utils.get_dict_value(candle_dict, 'start')
        self.end = utils.get_dict_value(candle_dict, 'end')
        self.low = utils.get_dict_value(candle_dict, 'low')
        self.high = utils.get_dict_value(candle_dict, 'high')
        self.open = utils.get_dict_value(candle_dict, 'open')
        self.close = utils.get_dict_value(candle_dict, 'close')
        self.volume = utils.get_dict_value(candle_dict, 'volume')
