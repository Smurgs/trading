from Questrade import utils


class Account(object):

    def __init__(self, acc_dict):
        self.type = utils.get_dict_value(acc_dict, 'type')
        self.number = utils.get_dict_value(acc_dict, 'number')
        self.status = utils.get_dict_value(acc_dict, 'status')
        self.isPrimary = utils.get_dict_value(acc_dict, 'isPrimary')
        self.isBilling = utils.get_dict_value(acc_dict, 'isBilling')
        self.clientAccountType = utils.get_dict_value(acc_dict, 'clientAccountType')
