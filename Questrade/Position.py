from Questrade import utils


class Position(object):

    def __init__(self, position_dict):
        self.symbol = utils.get_dict_value(position_dict, 'symbol')
        self.symbolId = utils.get_dict_value(position_dict, 'symbolId')
        self.openQuantity = utils.get_dict_value(position_dict, 'openQuantity')
        self.closedQuantity = utils.get_dict_value(position_dict, 'closedQuantity')
        self.currentMarketValue = utils.get_dict_value(position_dict, 'currentMarketValue')
        self.currentPrice = utils.get_dict_value(position_dict, 'currentPrice')
        self.averageEntryPrice = utils.get_dict_value(position_dict, 'averageEntryPrice')
        self.closedPnL = utils.get_dict_value(position_dict, 'closedPnL')
        self.openPnL = utils.get_dict_value(position_dict, 'openPnL')
        self.totalCost = utils.get_dict_value(position_dict, 'totalCost')
        self.isRealTime = utils.get_dict_value(position_dict, 'isRealTime')
        self.isUnderReorg = utils.get_dict_value(position_dict, 'isUnderReorg')
