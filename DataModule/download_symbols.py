#!/usr/local/bin/python3

import os
import json
import time
import logging

import definitions
from DataModule.DataManager import DataManager
from Questrade.QuestradeWrapper import QuestradeAuthenticationError


# Setup logger
fmt = '%(asctime)s - [%(levelname)s] - %(message)s'
datefmt = '%d-%b-%y %H:%M:%S'
log_file = os.path.join(definitions.ROOT_DIR, 'logs/download_log.txt')
logging.basicConfig(format=fmt, datefmt=datefmt, level=logging.INFO, filename=log_file)
logging.getLogger().addHandler(logging.StreamHandler())


def main():
    logger = logging.getLogger()
    logger.info('############################### Starting download script ###############################')
    error_flag = False

    while True:

        # Get symbols to download
        logger.info('Collecting symbols from file')
        try:
            with open(os.path.join(os.path.dirname(__file__), 'symbols.json')) as infile:
                f = json.load(infile)
            symbols = set(f['djia'] + f['tech'] + f['etf'])
        except IOError:
            error_flag = True
            logger.exception('Failed to load symbols to download. Quitting')
            break

        # Instantiate DataManager
        logger.info('Creating DataManager')
        try:
            dm = DataManager()
        except NotADirectoryError:
            error_flag = True
            logger.exception('Failed in create DataManager. Quitting')
            break

        # Download symbols
        logger.info('Starting download')
        count = 0
        for symbol in symbols:
            count += 1
            logger.info('Downloading %s -- %d/%d' % (symbol, count, len(symbols)))
            try:
                dm.download(symbol)
            except QuestradeAuthenticationError:
                error_flag = True
                logger.exception('Failed to authenticate with Questrade. Quitting')
                break
            except Exception:
                error_flag = True
                logger.exception('Failed to download %s' % symbol)
            time.sleep(1)
        break

    # Send pass/fail notification
    title = 'Data Download Report'
    text = 'FAIL' if error_flag else 'PASS'
    os.system("""
                  osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))


if __name__ == '__main__':
    main()
