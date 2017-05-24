import csv
import os
import sys
sys.path.append("..")
from conf import stock_day_line_file
from conf import stock_oneday_line_file


#date = str(input('pls input the end date for spider(xxxx-xx-xx): '))
#file_write = open(stock_oneday_line_file + 'allinone.csv','w')
file_write = csv.writer(open(stock_oneday_line_file + 'allinone.csv','w'))

for dir,floder,files in os.walk(stock_day_line_file):
    for file in files:
        file_open = stock_day_line_file + file
        alldata = csv.reader(open(file_open),delimiter=',')
        for line in alldata:
            line.insert(0,file[:-4])
            #print(line)
            file_write.writerow(line)
       
