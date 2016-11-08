import sys
sys.path.append("..")
from getstocklist import getstocklist
from getstockdayline import getstockdayline
from core import depickle_stock_list



def main():
    getstocklist()
    print('[+]更新股票代码完成')
    print('[+]开始更新股票日线数据... ...')
    
    getstockdayline(depickle_stock_list())
    print('[+]股票日线数据更新完毕')
    
def main2():
    stocklist = ['601186']
    getstockdayline(stocklist)
    print('[+]股票日线数据更新完毕')    

main()