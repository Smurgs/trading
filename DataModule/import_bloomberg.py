import os
import xlrd
from datetime import datetime

from DataModule.Data import Data
from DataModule.DataFrame import DataFrame
from DataModule.DataManager import DataManager

symbol = 'AAPL'
data_root_dir = '/localdisk/trading/Database/_Bloomberg/AAPL/'


def main():
    dm = DataManager()

    # Get all file paths in subdirectories
    file_paths = []
    for path, subdirs, files in os.walk(data_root_dir):
        for name in files:
            file_paths.append(os.path.join(path, name))

    for file_path in file_paths:
        print('Importing ' + file_path)

        workbook = xlrd.open_workbook(file_path)
        sheet = workbook.sheet_by_index(0)

        data_frames = []
        for i in range(sheet.nrows):
            line = sheet.row_values(i)

            if 'Time' in line[0] or 'Summary' in line[0]:
                continue

            if '' == line[-1]:
                date = line[0][:9]
                date = datetime.strptime(date, '%d%b%Y')
                continue

            # Create DataFrame
            start_hour = int(line[0][:2])
            start_min = int(line[0][3:5])
            start = datetime(date.year, date.month, date.day, start_hour, start_min)
            end_hour = int(line[0][8:10])
            end_min = int(line[0][11:13])
            end = datetime(date.year, date.month, date.day, end_hour, end_min)
            close = float(line[1])
            open = float(line[3])
            high = float(line[4])
            low = float(line[5])
            volume = 0 if type(line[7]) == str else int(line[7])
            data_frames.append(DataFrame(start, end, open, high, low, close, volume))

        dm._store_data(Data(symbol, Data.Interval.ONE_MIN, data_frames))


if __name__ == '__main__':
    main()
