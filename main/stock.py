from datetime import datetime
import time
import shlex
import subprocess
import os
import sys
sys.path.append("..")
from strategy import jasonshortmain
from spider import getstocklist
from spider import getstockdayline
from core import get_stock_market
from conf import stock_day_line_file
from core import depickle_stock_list

def timetosleep():
    
    curTime = datetime.now()
    desTime = curTime.replace(hour=20, minute=0, second=0, microsecond=0)
    delta = desTime - curTime
    skipSeconds =  delta.total_seconds()
    return skipSeconds



#每天定时更新股票代码
time.sleep(timetosleep())
print('[+]开始更新股票代码')
getstocklist.getstocklist()
print('[+]更新股票代码完成')
time.sleep(3)

#更新股票数据
print('[+]开始更新全面股票数据... ...')
getstockdayline.getstockdayline(depickle_stock_list())
print('[+]全面股票数据更新完成，开始纠错... ...')

error_file = open('error-UPDATE.log','r')
errlist = error_file.readlines()
errlist = [x[:-1] for x in errlist]
error_file.close()
time.sleep(3)
for code in (errlist):
    prefix = get_stock_market(code)
    file = stock_day_line_file + prefix + code + '.csv'
    if os.path.exists(file):
        os.remove(file)
        print('del '+file)
getstockdayline.getstockdayline(errlist)
print('[+]纠错完成，开始计算jasonshort策略... ...')

#计算jasonshort策略
jasonshortmain.runjasonshort()
print('[+]完毕')

#git部分
cwd = "D:\\Users\\zhouyu835\\Downloads\\git\\stock"
cmd = "git add -A"
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git commit -m 'update output jasonshort'"
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git push origin master"

def gitpush():
    try:
        time.sleep(5)
        subprocess.check_output(shlex.split(cmd), cwd=cwd)
    except:
        gitpush()

gitpush()