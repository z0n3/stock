import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv
import time
import os
import sys
sys.path.append("..")
from conf import stock_day_line_url
from conf import stock_day_line_file
from conf import stock_day_line_headers
from core import get_stock_market



def getstockdaylineupdate(code,year,season,file,lasteddate,stop_catch):
    #print('2',code,lasteddate,type(lasteddate))
    #global stop_catch
    stop_catch = stop_catch
    req = requests.get(stock_day_line_url.format(code,year,season))
    bs_url = bs(req.text, "lxml")
    table = bs_url.find(id = 'FundHoldSharesTable')
    
    csv_write = open(file,'a',encoding = 'utf8')
    title = True
    line_count = 0
    for row in table.find_all("tr"):
        if len(row) == 3:
            continue
        if title:
            title = False
            continue
        for cells in row.find_all("td"):
            for cell in cells.find_all("div"):
                if cell.getText().strip() == lasteddate:
                    #print(type(cell.getText().strip()),'aaaaaaaaaaaaaaaa')
                    stop_catch = True
                    return(stop_catch)
                csv_write.write(cell.getText().strip())
            csv_write.write(',')
        csv_write.write('\n')
        line_count += 1
    csv_write.close()  
    
    return(stop_catch)


def getstockdayline(stocklist):
    #删除0字节文件
    for code in (stocklist):
        prefix = get_stock_market(code)
        file = stock_day_line_file + prefix + code + '.csv'
        if os.path.exists(file):
            if os.path.getsize(file) == 0:
                #print(file)
                os.remove(file)
    time.sleep(5)
    
    error_file = open('error-UPDATE.log','w')
    for code in (stocklist):
        stop_catch = False
        prefix = get_stock_market(code)
        file = stock_day_line_file + prefix + code + '.csv'
        #读取已下载最新日期
        if os.path.exists(file):
            alldata = pd.read_csv(file,names = stock_day_line_headers)
            lasteddate = alldata.iloc[0]['date'] 
            #print((lasteddate))
        else:
            lasteddate = '1990-12-19'
        #print(code,lasteddate,type(lasteddate))
        if prefix in ['sh','sz']:
            try:
                for year in range(2016,1989,-1):#1989
                    for season in range(4,0,-1):
                        if stop_catch:
                            break
                        #print(year,season,stop_catch)
                        stop_catch = getstockdaylineupdate(code,year,season,file,lasteddate,stop_catch)
                    if stop_catch:
                        break
            except Exception as e:
                error_file.write(code+'\n')
                print(e)
                error_file.flush()
            #重新排序
            alldata = csv.reader(open(file),delimiter=',')
            sortedlist = sorted(alldata, key = lambda x: (x[0]),reverse = True)
            with open(file, "w", newline = '') as f:
                fileWriter = csv.writer(f, delimiter=',')
                for row in sortedlist:
                    fileWriter.writerow(row)
        
    error_file.close()


