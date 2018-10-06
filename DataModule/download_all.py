import os
import json
import time
import logging
from datetime import datetime

from DataModule.DataManager import DataManager


def main():
    LOGGER = logging.getLogger()
    LOGGER.info('Download all script starting up....')

    with open(os.path.join(os.path.dirname(__file__), 'symbols.json')) as infile:
        f = json.load(infile)
    indexes = f['indexes']
    sp500 = f['sp500']

    dm = DataManager()
    today = datetime.today()
    for symbol in indexes + sp500:

        # Skip if we already downloaded today
        daily_path = dm.build_file_path(symbol, today.year)
        minute_path = dm.build_file_path(symbol, today.year, today.month)
        if os.path.isfile(daily_path) and os.path.isfile(minute_path):

            # Get last storage date of daily data
            with open(daily_path) as infile:
                daily_json = json.load(infile)
            daily_last = datetime.strptime(daily_json['meta']['date_stored'], '%Y-%m-%d %H:%M')

            # Get last storage date of minute data
            with open(minute_path) as infile:
                minute_json = json.load(infile)
            minute_last = datetime.strptime(minute_json['meta']['date_stored'], '%Y-%m-%d %H:%M')

            if today.year == daily_last.year == minute_last.year:
                if today.month == daily_last.month == minute_last.month:
                    if today.day == daily_last.day == minute_last.day:
                        LOGGER.info('Skipping %s' % symbol)
                        continue

        LOGGER.info('Downloading %s' % symbol)
        dm.download(symbol)
        time.sleep(15)


if __name__ == '__main__':
    main()
