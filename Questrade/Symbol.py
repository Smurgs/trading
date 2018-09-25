from Questrade import utils


class Symbol(object):

    def __init__(self, symbol_dict):
        self.symbol = utils.get_dict_value(symbol_dict, 'symbol')
        self.symbolId = utils.get_dict_value(symbol_dict, 'symbolId')
        self.description = utils.get_dict_value(symbol_dict, 'description')
        self.securityType = utils.get_dict_value(symbol_dict, 'securityType')
        self.listingExchange = utils.get_dict_value(symbol_dict, 'listingExchange')
        self.isTradable = utils.get_dict_value(symbol_dict, 'isTradable')
        self.isQuotable = utils.get_dict_value(symbol_dict, 'isQuotable')
        self.currency = utils.get_dict_value(symbol_dict, 'currency')
