import os
import json
import shutil
from datetime import datetime
import time

import definitions
from DataModule.OptionData import OptionData
from DataModule.OptionDataFrame import OptionDataFrame
from Questrade import QuestradeWrapper


class OptionDataManager(object):

    def __init__(self, database_dir=definitions.DATABASE_DIR):
        self.database_dir = database_dir
        if not os.path.isdir(self.database_dir):
            raise NotADirectoryError('Database directory does not exist: %s' % self.database_dir)

    def download(self, symbol):
        """Download current option quotes for all expiry dates and strike prices

            Args:
                symbol (str): Stock symbol for requested data (ex. 'FB')
        """
        print('Authenticating with Questrade')
        # Authenticate with Questrade
        qw = QuestradeWrapper()
        qw.authenticate()

        # Establish quote time
        now = datetime.today()
        quote_time = datetime(now.year, now.month, now.day, now.hour, now.minute - (now.minute % 5))

        # Get all call and put option symbol ids
        print('Getting call and put ids')
        option_ids = []
        sym = qw.search_symbol(symbol)
        option_chain = qw.get_options_ids(sym.symbolId)
        option_chain = option_chain['optionChain']
        for expiry_chain in option_chain:
            if 'chainPerRoot' in expiry_chain:
                if len(expiry_chain['chainPerRoot']) > 0:
                    if 'chainPerStrikePrice' in expiry_chain['chainPerRoot'][0]:
                        for strike_chain in expiry_chain['chainPerRoot'][0]['chainPerStrikePrice']:
                            if 'callSymbolId' in strike_chain:
                                option_ids.append(strike_chain['callSymbolId'])
                            if 'putSymbolId' in strike_chain:
                                option_ids.append(strike_chain['putSymbolId'])

        # Download option quotes in chunks of 100
        print('Downloading option quotes')
        option_quotes = []
        start_indices = range(0, len(option_ids), 100)
        end_indices = range(100, len(option_ids) + 100, 100)
        for i in range(len(start_indices)):
            option_quotes.append(qw.get_market_option_quote(option_ids[start_indices[i]:end_indices[i]]))

        # Store option quotes
        print('Storing option quotes')
        for option_quote in option_quotes:
            self._store_quotes(option_quote, quote_time)

    def build_file_path(self, symbol, expiry, strike, option_type):
        expiry_str = '%d_%02d_%02d' % (expiry.year, expiry.month, expiry.day)
        file_path = os.path.join(self.database_dir, symbol)
        file_path = os.path.join(file_path, 'options')
        file_path = os.path.join(file_path, expiry_str)
        file_path = os.path.join(file_path, symbol + '_' + expiry_str + '_' + str(strike) + '_' + option_type + '.json')
        return file_path

    def _load_file(self, symbol, expiry, strike, option_type):
        # Get file path
        file_path = self.build_file_path(symbol, expiry, strike, option_type)

        # Check if file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError('Could not load desired data for %s' % file_path)

        # Load file
        with open(file_path) as infile:
            file_data = OptionData.from_dict(json.load(infile))
        return file_data

    def _store_quotes(self, option_quotes, quote_time):
        backup_suffix = '.backup'

        for option_quote in option_quotes:

            # Get quote details and build OptionDataFrame
            symbol = option_quote.underlying
            info = option_quote.symbol.replace(symbol, '')
            if 'C' in info:
                info = info.split('C')
                option_type = 'C'
            else:
                info = info.split('P')
                option_type = 'P'
            expiry = datetime.strptime(info[0], '%d%b%y')
            strike = info[1]
            quote_frame = OptionDataFrame.from_option_quote(option_quote, quote_time)

            # If file exists (usually the case), add to file
            file_path = self.build_file_path(symbol, expiry, strike, option_type)
            if os.path.isfile(file_path):

                # Check if backup also exists (only when previous store was interrupted)
                if os.path.isfile(file_path + backup_suffix):

                    # If old target is largest, remove backup
                    if os.path.getsize(file_path) >= os.path.getsize(file_path + backup_suffix):
                        os.remove(file_path + backup_suffix)

                    # Else backup is largest, copy to target and remove backup
                    else:
                        shutil.copyfile(file_path + backup_suffix, file_path)
                        os.remove(file_path + backup_suffix)

                # Copy old target to backup
                shutil.copyfile(file_path, file_path + backup_suffix)

                # Combined old and new data
                old = self._load_file(symbol, expiry, strike, option_type)
                file_data = OptionData(symbol, expiry, strike, option_type, old.frames + [quote_frame])

                # Delete old target
                os.remove(file_path)

            else:
                # Prepare new data
                file_data = OptionData(symbol, expiry, strike, option_type, [quote_frame])

            # Write new target
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            data_to_serialize = OptionData.to_dict(file_data)
            data_to_serialize['meta']['date_stored'] = datetime.today().strftime("%Y-%m-%d %H:%M")
            with open(file_path, 'w+') as outfile:
                json.dump(data_to_serialize, outfile)

            # Delete backup (if exists)
            if os.path.isfile(file_path + backup_suffix):
                os.remove(file_path + backup_suffix)


if __name__ == '__main__':
    start = time.time()
    dm = OptionDataManager('/localdisk/trading/testdb')
    dm.download('SPY')
    dm.download('QQQ')
    dm.download('AAPL')
    dm.download('MSFT')
    dm.download('GOOGL')
    end = time.time()
    print('Runtime')
    print(end - start)
    exit(1)
