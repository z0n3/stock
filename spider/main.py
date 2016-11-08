import os
import sys
sys.path.append("..")
from getstocklist import getstocklist
from getstockdayline import getstockdayline
from core import depickle_stock_list
from core import get_stock_market
from conf import stock_day_line_file



def main():
    getstocklist()
    print('[+]更新股票代码完成')
    print('[+]开始更新股票日线数据... ...')
    
    getstockdayline(depickle_stock_list())
    print('[+]股票日线数据更新完毕')
    
def main2():
    stocklist = ['300561','000728','600333','002221','603618','002449','000910','600422','002668','002562','002692','600844','300349','000625','300423','002729','002063','300241','300163','603067']
    #删除出错文件
    for code in (stocklist):
        prefix = get_stock_market(code)
        file = stock_day_line_file + prefix + code + '.csv'
        if os.path.exists(file):
            os.remove(file)
            print('del '+file)
    getstockdayline(stocklist)
    print('[+]股票日线数据更新完毕')    

main2()