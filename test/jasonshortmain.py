import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append("..")
from core import Stock
from core import depickle_stock_list

#todo:
#增加趋势的分析



#temp
stocklist = ['601218','601933']

class jasonshort(Stock):
    '''
    backtest base at the sell day
    descript
    '''
    def __init__(self,code,stopgain=0.05,stoploss=-0.02,holdday=3):
        Stock.__init__(self,code)
        self.ma(5)
        self.ma(10)
        self.macd(12,26,9)
        
    def test(self):
        #金叉
        self.stockdayline['goldif'] = (self.stockdayline['5dma'] > self.stockdayline['10dma']) & (self.stockdayline['5dma'].shift(1) < self.stockdayline['10dma'].shift(1))
        #前13天均线无交叉
        self.stockdayline['crossiftmp'] = ((self.stockdayline['5dma'] - self.stockdayline['10dma']) * (self.stockdayline['5dma'].shift(1) - self.stockdayline['10dma'].shift(1))) < 0
        self.stockdayline['crossif'] = (self.stockdayline['crossiftmp'].shift(1).rolling(center=False,window=13).sum() == 0)
        #MACD>-0.01
        self.stockdayline['macdif'] = (self.stockdayline['macd'] > -0.01)
        #MACD背离
        self.stockdayline['minclose'] = self.stockdayline['close'].rolling(center=False,window=13).apply(lambda x:pd.Series(x).idxmin())
        self.stockdayline['minmacd'] = self.stockdayline['macd'].rolling(center=False,window=13).apply(lambda x:pd.Series(x).idxmin())
        self.stockdayline['beiliif'] = ((self.stockdayline['minclose'] - self.stockdayline['minmacd']) > 2)
        
        #
        self.stockdayline['yz'] = (self.stockdayline['goldif'] & self.stockdayline['crossif'] & self.stockdayline['macdif'] & self.stockdayline['beiliif'])
        


def main():
    file = open('allcodejasonshort.log','w')
    for code in depickle_stock_list():
        try:
            a=jasonshort(code)
            a.test()
            b=a.stockdayline[a.stockdayline['yz']==True]['yz']
            file.write(code+'\n'+str(b)+'\n\n')
        except Exception as e:
            pass
    file.close()

def main2():
    file2 = open('jasonshorttoday.log','w')
    today = '2016-10-28 00:00:00'#2016-10-25'
    for code in depickle_stock_list():
        try:
            a=jasonshort(code)
            a.test()
            b=a.stockdayline[a.stockdayline['yz']==True]['yz']
            if (str(b[-1:].index[0])) == today:
                file2.write(code+'\n')
        except:
            pass
    file2.close()
#a=jasonshort('002797')
#a.test()
#a.stockdayline.to_csv('b.csv')

    
main2()
    