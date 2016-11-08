import pandas as pd
import sys
sys.path.append("..")
from core import Stock
from core import depickle_stock_list
from core import get_stock_market
from teststrategy import teststrategy
from teststrategy import holdgainloss


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
        del self.stockdayline['crossiftmp']     
        #MACD>-0.01
        self.stockdayline['macdif'] = (self.stockdayline['macd'] > -0.01)
        #MACD背离
        self.stockdayline['minclose'] = self.stockdayline['close'].rolling(center=False,window=13).apply(lambda x:pd.Series(x).idxmin())
        self.stockdayline['minmacd'] = self.stockdayline['macd'].rolling(center=False,window=13).apply(lambda x:pd.Series(x).idxmin())
        self.stockdayline['beiliif'] = ((self.stockdayline['minclose'] - self.stockdayline['minmacd']) > 2)
        del self.stockdayline['minclose'] 
        del self.stockdayline['minmacd'] 
        #
        self.stockdayline['yz'] = (self.stockdayline['goldif'] & self.stockdayline['crossif'] & self.stockdayline['macdif'] & self.stockdayline['beiliif'])
        

def main():
    file = open('jasonshortmain.log','w')
    file2 = open('jasonshortmaindetail.log','w')
    for code in depickle_stock_list():
        if get_stock_market(code) in ['sh','sz']:
            try:
                a=jasonshort(code)
                a.test()
                b=teststrategy(a.stockdayline)
                c=(b+1).cumprod()
                file.write(code+','+'{:.5f}'.format(c[-1:][0])+','+'{:.5f}'.format(b[b>0].count()/b.count())+','+'{:.5f}'.format(b.std())+'\n')
                file2.write(code+'\n'+str(b)+'\n\n')                
                #b.to_csv('a.csv')
            except Exception as e:
                pass                
                #print(code,e)
    file.close()
    file2.close()
    

def holdmaxgainloss():
    file = open('holdgainloss.log','w')
    for code in depickle_stock_list():
        if get_stock_market(code) in ['sh','sz']:
            try:
                a=jasonshort(code)
                a.test()
                b=holdgainloss(a.stockdayline)
                file.write(code+'\n'+str(b)+'\n\n')                
                #b.to_csv('a.csv')
            except Exception as e:
                #pass                
                print(code,e)
    file.close()

#a=jasonshort('002797')
#a.test()
#a.stockdayline.to_csv('b.csv')

    
holdmaxgainloss()
    