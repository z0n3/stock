import pandas as pd
import sys
sys.path.append("..")
from conf import stock_day_line_headers
from core import get_stock_market
from core import depickle_stock_list
from anlscore import Stock

class Short100(Stock):
    '''
    backtest base at the sell day
    descript
    '''
    def __init__(self,code):
        Stock.__init__(self,code)
        self.openrev()
        self.shallowup()
        self.ma(5)
        self.ma(10)
        self.ma(20)

    def days3db7(self):
        '''
        三天跌幅超过7%，第四天涨3%以内，并且收红，第五天开盘买入，第六天开盘卖出
        '''
        self.stockdayline['days3db7'] = (((self.stockdayline['close'].shift(3) / self.stockdayline['close'].shift(6) - 1) <= -0.07) 
        & (self.stockdayline['close'].shift(2) > self.stockdayline['open'].shift(2))
        & (self.stockdayline['shallowup'].shift(2))
        & (self.stockdayline['5dma'] > self.stockdayline['20dma'])
        & (self.stockdayline['close'].shift(2) > self.stockdayline['5dma'].shift(2))
        )
        

'''
#test
a=Short100('600080')
a.days3db7()
b=a.stockdayline[a.stockdayline['days3db7']==True]['openrev']
print(b.describe())
print(b.sum())
print(a.stockdayline[a.stockdayline['days3db7']==True])
'''
log_file = open('days3db7.log','w')
geshu = 0
for code in (depickle_stock_list()):
    prefix = get_stock_market(code)
    if prefix in ['sh','sz']:
        try:
            a=Short100(code)
            a.days3db7()
            del a.stockdayline['low']
            del a.stockdayline['high']
            del a.stockdayline['vol']
            del a.stockdayline['amount']
            b=a.stockdayline[a.stockdayline['days3db7']==True]['openrev']
            log_file.write(code+'\t')
            log_file.write(str(a.stockdayline[a.stockdayline['days3db7']==True]['openrev'].sum()))
            log_file.write('\t')
            log_file.write(str(len(b[b>0])))
            log_file.write('\t')
            log_file.write(str(len(b[b<0])))
            log_file.write(',\r')
            log_file.flush()
        except Exception as e:
            pass
log_file.close()