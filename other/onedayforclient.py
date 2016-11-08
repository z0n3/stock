# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 22:02:57 2016

@author: j
"""
import csv
"""
print('*'*62)
print('***               精确量化数据 请认准量化基因')
print('***')
print('***使用说明：')
print('***请将本程序与历史日线数据、当日日线数据文件放在同一文件夹内，')
print('***当日日线数据文件文件名格式必须为yyyy-mm-dd.csv')
print('***按格式要求输入日期后按回车键执行。')
print('*'*62)
"""
date = str(input('\nPls input the date(yyyy-mm-dd): '))

try:
    file_open = open(date + '.csv')
    print('\n[+]Starting... ... pls waiter a monment')
    for line in file_open.readlines():
        data = line.split(',')
        file_write = open(data[0] + '.csv','a')
        for d in data[1:-1]:
            file_write.write(d + ',')
        file_write.write('\n')
        file_write.close()
        #重新排序
        alldata = csv.reader(open(data[0] + '.csv'),delimiter=',')
        sortedlist = sorted(alldata, key = lambda x: (x[0]),reverse = True)
        with open(data[0] + '.csv', "w", newline = '') as f:
            fileWriter = csv.writer(f, delimiter=',')
            for row in sortedlist:
                fileWriter.writerow(row)
        
    file_open.close()
    print('[+]done!')
except:
    print('\n\n[!]Pls check the date you input.')

input('')