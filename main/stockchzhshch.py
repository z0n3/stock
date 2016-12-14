from datetime import datetime
import time
import shlex
import subprocess
import sys
sys.path.append("..")
from spider import getstocklist
from spider import getstockfzline
from strategy import chzhshch
from core import depickle_stock_list


print('[+]开始更新股票代码')
getstocklist.getstocklist()
print('[+]更新股票代码完成')
time.sleep(3)

#更新股票数据
print('[+]开始更新全面股票数据... ...')
getstockfzline.getstockfzline(depickle_stock_list())
print('[+]全面股票数据更新完成，开始计算策略... ...')



#log file句柄
strtoday = datetime.now().strftime('%Y%m%d')
logfile = open('{}_chzhshch.log'.format(strtoday),'w')
#计算chzhshch策略
chzhshch.runchzhshch(logfile)


logfile.close()
print('[+]完毕')

#git部分
cwd = "D:\\Users\\zhouyu835\\Downloads\\git\\stock"
cmd = "git add -A"
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git commit -m 'update strategy chzhshch output {}'".format(strtoday)
subprocess.check_output(shlex.split(cmd), cwd=cwd)
cmd = "git push origin master"

def gitpush():
    try:
        time.sleep(5)
        subprocess.check_output(shlex.split(cmd), cwd=cwd)
    except:
        gitpush()

gitpush()
