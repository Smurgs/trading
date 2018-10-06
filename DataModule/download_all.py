import os
import json
import time

from DataModule.DataManager import DataManager


def main():
    with open(os.path.join(os.path.dirname(__file__), 'symbols.json')) as infile:
        f = json.load(infile)
    indexes = f['indexes']
    sp500 = f['sp500']

    dm = DataManager()
    for symbol in indexes + sp500:
        dm.download(symbol)
        time.sleep(15)


if __name__ == '__main__':
    main()

