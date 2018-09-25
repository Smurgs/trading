from Questrade import utils


class OptionQuote(object):

    def __init__(self, quote_dict):
        self.underlying = utils.get_dict_value(quote_dict, 'underlying')
        self.underlyingId = utils.get_dict_value(quote_dict, 'underlyingId')
        self.symbol = utils.get_dict_value(quote_dict, 'symbol')
        self.symbolId = utils.get_dict_value(quote_dict, 'symbolId')
        self.bidPrice = utils.get_dict_value(quote_dict, 'bidPrice')
        self.bidSize = utils.get_dict_value(quote_dict, 'bidSize')
        self.askPrice = utils.get_dict_value(quote_dict, 'askPrice')
        self.askSize = utils.get_dict_value(quote_dict, 'askSize')
        self.lastTradeTrHrs = utils.get_dict_value(quote_dict, 'lastTradeTrHrs')
        self.lastTradePrice = utils.get_dict_value(quote_dict, 'lastTradePrice')
        self.lastTradeSize = utils.get_dict_value(quote_dict, 'lastTradeSize')
        self.lastTradeTick = utils.get_dict_value(quote_dict, 'lastTradeTick')
        self.lastTradeTime = utils.get_dict_value(quote_dict, 'lastTradeTime')
        self.volume = utils.get_dict_value(quote_dict, 'volume')
        self.openPrice = utils.get_dict_value(quote_dict, 'openPrice')
        self.highPrice = utils.get_dict_value(quote_dict, 'highPrice')
        self.lowPrice = utils.get_dict_value(quote_dict, 'lowPrice')
        self.volatility = utils.get_dict_value(quote_dict, 'volatility')
        self.delta = utils.get_dict_value(quote_dict, 'delta')
        self.gamma = utils.get_dict_value(quote_dict, 'gamma')
        self.theta = utils.get_dict_value(quote_dict, 'theta')
        self.vega = utils.get_dict_value(quote_dict, 'vega')
        self.rho = utils.get_dict_value(quote_dict, 'rho')
        self.openInterest = utils.get_dict_value(quote_dict, 'openInterest')
        self.delay = utils.get_dict_value(quote_dict, 'delay')
        self.isHalted = utils.get_dict_value(quote_dict, 'isHalted')
        self.VWAP = utils.get_dict_value(quote_dict, 'VWAP')
