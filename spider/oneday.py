import csv
import os
import sys
sys.path.append("..")
from conf import stock_day_line_file
from conf import stock_oneday_line_file


date = str(input('pls input the date for spider(xxxx-xx-xx): '))
file_write = open(stock_oneday_line_file + date + '.csv','w')

for dir,floder,files in os.walk(stock_day_line_file):
    for file in files:
        file_open = stock_day_line_file + file
        alldata = csv.reader(open(file_open),delimiter=',')
        sortedlist = sorted(alldata, key = lambda x: (x[0]),reverse = True)
        try:
            for sorteddata in sortedlist:
                if sorteddata[0] == date:
                    file_write.write(file[:-4])
                    for d in sorteddata:
                        file_write.write(',' + str(d))
                    file_write.write('\n')
                    break
        except:
            pass
file_write.close()
