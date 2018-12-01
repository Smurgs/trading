import os
import json
import time
from datetime import datetime

from DataModule.OptionDataManager import OptionDataManager


def main():
    print('###################################')
    print('Starting download options script...')

    with open(os.path.join(os.path.dirname(__file__), 'symbols.json')) as infile:
        f = json.load(infile)
    options_symbols = f['options']

    dm = OptionDataManager('/localdisk/trading/testdb')

    today = datetime.today()
    exe_times = [datetime(today.year, today.month, today.day, 9, x) for x in range(30, 56, 5)]
    exe_times += [datetime(today.year, today.month, today.day, y, x) for y in range(10, 16) for x in range(0, 56, 5)]
    cycle_count = 0
    for exe_time in exe_times:
        cycle_count += 1
        count = 0

        # Sleep until exe time
        if (exe_time - datetime.today()).days == 0:
            time.sleep((exe_time - datetime.today()).seconds)

        print('Starting cycle %d' % cycle_count)
        print(exe_time)
        for symbol in options_symbols:
            count += 1
            print('Downloading %s -- %d/%d' % (symbol, count, len(options_symbols)))
            dm.download(symbol)


if __name__ == '__main__':
    main()
