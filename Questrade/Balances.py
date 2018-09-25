from Questrade import utils


class Balance(object):

    def __init__(self, balance_dict):
        self.currency = utils.get_dict_value(balance_dict, 'currency')
        self.cash = utils.get_dict_value(balance_dict, 'cash')
        self.marketValue = utils.get_dict_value(balance_dict, 'marketValue')
        self.totalEquity = utils.get_dict_value(balance_dict, 'totalEquity')
        self.buyingPower = utils.get_dict_value(balance_dict, 'buyingPower')
        self.maintenanceExcess = utils.get_dict_value(balance_dict, 'maintenanceExcess')
        self.isRealTime = utils.get_dict_value(balance_dict, 'isRealTime')


class Balances(object):

    def __init__(self, balances_dict):
        self.perCurrencyBalances = [Balance(x) for x in utils.get_dict_value(balances_dict, 'perCurrencyBalances')]
        self.combinedBalances = [Balance(x) for x in utils.get_dict_value(balances_dict, 'combinedBalances')]
        self.sodPerCurrencyBalances = [Balance(x) for x in utils.get_dict_value(balances_dict, 'sodPerCurrencyBalances')]
        self.sodCombinedBalances = [Balance(x) for x in utils.get_dict_value(balances_dict, 'sodCombinedBalances')]