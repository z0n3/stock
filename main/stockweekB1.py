from datetime import datetime
import time
import shlex
import subprocess
import sys
sys.path.append("..")
from spider import getstocklist
from spider import getstocktdxdayline
from strategy import chzhshchweekB1
from core import depickle_stock_list

trade = input("Is it workday? (y/n):    ")
if trade != "n":
    trading = True
else:
    trading = False
        
print('[+]开始更新股票代码')
#getstocklist.getstocklist()
print('[+]更新股票代码完成')
time.sleep(3)

#更新股票数据
print('[+]开始更新全面股票数据... ...')
getstocktdxdayline.getstocktdxdayline(depickle_stock_list())
print('[+]开始计算策略... ...')



#log file句柄
strtoday = datetime.now().strftime('%Y%m%d')
logfile = open('{}_chzhshch_week_B1_output.log'.format(strtoday),'w')
#计算chzhshch策略
chzhshchweekB1.runchzhshchweekB1(logfile,trading)
logfile.close()


print('[+]完毕')
'''
#git部分
cwd = "D:\\Users\\zhouyu835\\Downloads\\git\\stock"
#cwd = "C:\\Users\\Jason\\Downloads\\git\\stock"
cmd = "git add -A"
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git commit -m 'update strategy chzhshch_30m_jasonshort output {}'".format(strtoday)
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git push origin master"

def gitpush():
    try:
        time.sleep(5)
        subprocess.check_output(shlex.split(cmd), cwd=cwd)
    except:
        gitpush()

gitpush()
'''