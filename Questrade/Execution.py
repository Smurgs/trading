from Questrade import utils


class Execution(object):

    def __init__(self, execution_dict):
        self.symbol = utils.get_dict_value(execution_dict, 'symbol')
        self.symbolId = utils.get_dict_value(execution_dict, 'symbolId')
        self.quantity = utils.get_dict_value(execution_dict, 'quantity')
        self.side = utils.get_dict_value(execution_dict, 'side')
        self.price = utils.get_dict_value(execution_dict, 'price')
        self.id = utils.get_dict_value(execution_dict, 'id')
        self.orderId = utils.get_dict_value(execution_dict, 'orderId')
        self.orderChainId = utils.get_dict_value(execution_dict, 'orderChainId')
        self.exchangeExecId = utils.get_dict_value(execution_dict, 'exchangeExecId')
        self.timestamp = utils.get_dict_value(execution_dict, 'timestamp')
        self.notes = utils.get_dict_value(execution_dict, 'notes')
        self.venue = utils.get_dict_value(execution_dict, 'venue')
        self.totalCost = utils.get_dict_value(execution_dict, 'totalCost')
        self.orderPlacementCommission = utils.get_dict_value(execution_dict, 'orderPlacementCommission')
        self.commission = utils.get_dict_value(execution_dict, 'commission')
        self.executionFee = utils.get_dict_value(execution_dict, 'executionFee')
        self.secFee = utils.get_dict_value(execution_dict, 'secFee')
        self.canadianExecutionFee = utils.get_dict_value(execution_dict, 'canadianExecutionFee')
        self.parentId = utils.get_dict_value(execution_dict, 'parentId')
