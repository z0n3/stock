import csv
import os
import sys
sys.path.append("..")
from conf import stock_day_line_file
from conf import stock_oneday_line_file
from conf import stock_day_line_headers



cutdate = '2010-01-01'

for dir,floder,files in os.walk(stock_day_line_file):
    for file in files:
        file_open = stock_day_line_file + file
        alldata = csv.reader(open(file_open),delimiter=',')
        sortedlist = sorted(alldata, key = lambda x: (x[0]),reverse = True)
        index = 0
        for i in range(len(sortedlist)):
            if sortedlist[i][0] < cutdate:
                index = 0
                break
        sortedlist = sortedlist[i:]
        #print(stock_oneday_line_file + 'cut2016_' + file)
        with open(stock_oneday_line_file + 'cut2010_' + file, "w", newline = '') as f:
            fileWriter = csv.writer(f, delimiter=',')
            fileWriter.writerow(stock_day_line_headers)
            for row in sortedlist:
                fileWriter.writerow(row)
