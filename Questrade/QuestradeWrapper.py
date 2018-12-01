import os
import json
from datetime import datetime

from Questrade import *
from Questrade.Symbol import Symbol
from Questrade.OptionQuote import OptionQuote

import requests

config_file = os.path.join(os.path.dirname(__file__), 'config')
auth_url = 'https://login.questrade.com/oauth2/token'


class QuestradeWrapper(object):

    def __init__(self):
        self.access_token = None
        self.api_server = None
        self.token_type = None

    def _get_json(self, uri):
        r = requests.get(uri, headers={'Authorization': self.token_type + ' ' + self.access_token})
        return r.json()

    def _post_json(self, uri, data):
        r = requests.post(uri, json=data, headers={'Authorization': self.token_type + ' ' + self.access_token})
        return r.json()

    def authenticate(self):
        with open(config_file) as f:
            data = json.load(f)
        refresh_token = data['refresh_token']

        params = dict(grant_type='refresh_token', refresh_token=refresh_token)
        r = requests.get(url=auth_url, params=params)
        if r.status_code != 200:
            raise QuestradeAuthenticationError('Failed to authenticate with Questrade')
        data = r.json()
        with open(config_file, 'w') as f:
            json.dump(data, f)

        self.access_token = data['access_token']
        self.api_server = data['api_server']
        self.token_type = data['token_type']
        return True

    def set_refresh_token(self, token):
        with open(config_file) as f:
            data = json.load(f)
        data['refresh_token'] = token
        with open(config_file, 'w') as f:
            json.dump(data, f)

    def get_time(self):
        data = self._get_json('%sv1/time' % self.api_server)
        return data['time']

    def get_accounts(self):
        data = self._get_json('%sv1/accounts' % self.api_server)
        accounts = [Account(x) for x in data['accounts']]
        return accounts

    def get_positions(self, acc_id):
        data = self._get_json('%sv1/accounts/%s/positions' % (self.api_server, str(acc_id)))
        return [Position(x) for x in data['positions']]

    def get_account_balances(self, acc_id):
        data = self._get_json('%sv1/accounts/%s/balances' % (self.api_server, str(acc_id)))
        return Balances(data)

    def get_executions(self, acc_id):
        data = self._get_json('%sv1/accounts/%s/executions' % (self.api_server, str(acc_id)))
        return [Execution(x) for x in data['executions']]

    def get_orders(self, acc_id):
        pass

    def get_activities(self, acc_id):
        pass

    def get_symbol(self, symbol_id):
        pass

    def search_symbol(self, ticker):
        data = self._get_json('%sv1/symbols/search?prefix=%s' % (self.api_server, ticker))
        return Symbol(data['symbols'][0])

    def get_options_ids(self, symbol_id):
        data = self._get_json('%sv1/symbols/%s/options' % (self.api_server, str(symbol_id)))
        return data

    def get_market_quote(self, symbol_id):
        data = self._get_json('%sv1/markets/quotes/%s' % (self.api_server, str(symbol_id)))
        return [Quote(x) for x in data['quotes']]

    def get_market_option_quote(self, option_ids):
        payload = {'optionIds': option_ids}
        data = self._post_json('%sv1/markets/quotes/options' % self.api_server, payload)
        return [OptionQuote(x) for x in data['optionQuotes']]

    def get_candles(self, symbol, start, end, interval):
        uri = self.api_server + 'v1/markets/candles/' + str(symbol.symbolId) + '?'
        uri += 'startTime=' + start + '&'
        uri += 'endTime=' + end + '&'
        uri += 'interval=' + interval
        data = self._get_json(uri)
        return [Candle(x) for x in data['candles']]

    @staticmethod
    def datetime_to_string(dt):
        return '%d-%02d-%02dT%02d:%02d:00-04:00' % (dt.year, dt.month, dt.day, dt.hour, dt.minute)

    @staticmethod
    def string_to_datetime(s):
        return datetime.strptime(s[:-13], '%Y-%m-%dT%H:%M:%S')


class QuestradeAuthenticationError(Exception):
    pass


if __name__ == '__main__':
    qw = QuestradeWrapper()
    qw.authenticate()
    sym = qw.search_symbol('GOOGL')
    qw.get_options_ids(sym.symbolId)

