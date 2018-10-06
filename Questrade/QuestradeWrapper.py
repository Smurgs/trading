import os
import json
import requests
from datetime import datetime

from Questrade import *
from Questrade.Symbol import Symbol

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

    def authenticate(self):
        with open(config_file) as f:
            data = json.load(f)
        refresh_token = data['refresh_token']

        params = dict(grant_type='refresh_token', refresh_token=refresh_token)
        r = requests.get(url=auth_url, params=params)
        if r.status_code != 200:
            print('Failed to authenticate')
            return False

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
        #return [Symbol(x) for x in data['symbols']]

    def get_options(self, symbol_id):
        pass

    def get_market_quote(self, symbol_id):
        data = self._get_json('%sv1/markets/quotes/%s' % (self.api_server, str(symbol_id)))
        return [Quote(x) for x in data['quotes']]

    def get_market_option_quote(self, option_type, underlying_id, expiry_date, min_strike=None, max_strike=None):
        # TODO: Figure out how to post with a body
        data = self._get_json('%sv1/markets/quotes/options' % self.api_server)
        return [OptionQuote(x) for x in data['quotes']]

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


if __name__ == '__main__':
    qw = QuestradeWrapper()
    qw.authenticate()
    sym = qw.search_symbol('AAPL')
    start = datetime(2018, 10, 5)
    end = datetime(2018, 10, 6)
    response = qw.get_candles(sym, qw.datetime_to_string(start), qw.datetime_to_string(end), 'OneMinute')
    print([x.start for x in response])
    print(len(response))
