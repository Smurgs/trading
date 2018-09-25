from Questrade import utils


class Quote(object):

    def __init__(self, quote_dict):
        self.symbol = utils.get_dict_value(quote_dict, 'symbol')
        self.symbolId = utils.get_dict_value(quote_dict, 'symbolId')
        self.tier = utils.get_dict_value(quote_dict, 'tier')
        self.bidPrice = utils.get_dict_value(quote_dict, 'bidPrice')
        self.bidSize = utils.get_dict_value(quote_dict, 'bidSize')
        self.askPrice = utils.get_dict_value(quote_dict, 'askPrice')
        self.askSize = utils.get_dict_value(quote_dict, 'askSize')
        self.lastTradeTrHrs = utils.get_dict_value(quote_dict, 'lastTradeTrHrs')
        self.lastTradePrice = utils.get_dict_value(quote_dict, 'lastTradePrice')
        self.lastTradeSize = utils.get_dict_value(quote_dict, 'lastTradeSize')
        self.lastTradeTick = utils.get_dict_value(quote_dict, 'lastTradeTick')
        self.volume = utils.get_dict_value(quote_dict, 'volume')
        self.openPrice = utils.get_dict_value(quote_dict, 'openPrice')
        self.highPrice = utils.get_dict_value(quote_dict, 'highPrice')
        self.lowPrice = utils.get_dict_value(quote_dict, 'lowPrice')
        self.delay = utils.get_dict_value(quote_dict, 'delay')
        self.isHalted = utils.get_dict_value(quote_dict, 'isHalted')
