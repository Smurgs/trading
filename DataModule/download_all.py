import os
import json
import time
import logging

import definitions
from DataModule.DataManager import DataManager


def main():
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO,
                        filename=os.path.join(definitions.DATABASE_DIR, 'download_log'))

    LOGGER = logging.getLogger()
    LOGGER.info('Download all script starting up....')

    with open(os.path.join(os.path.dirname(__file__), 'symbols.json')) as infile:
        f = json.load(infile)
    indexes = f['indexes']
    sp500 = f['sp500']

    dm = DataManager()
    for symbol in indexes + sp500:
        LOGGER.info('Downloading %s' % symbol)
        dm.download(symbol)
        time.sleep(15)


if __name__ == '__main__':
    main()

