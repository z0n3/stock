import sys
sys.path.append("..")
from core import Stock
from core import depickle_stock_list

#temp
stocklist = ['600160']





class marun(Stock):
    '''
    backtest base at the sell day
    descript
    '''
    def __init__(self,code,stopgain=0.05,stoploss=-0.02,holdday=3):
        Stock.__init__(self,code)
        self.ma(5)
        self.ma(10)
        self.ma(20)
        self.volma(20)
        self.std()
        #验证数据
        self.stockdayline['buy']=self.stockdayline['open'].shift(-1)
        self.stockdayline['yz'] = 'tobeyz'
        
        for day in range(1,holdday+1):
            self.stockdayline['high/buy{}'.format(day)] = self.stockdayline['high'].shift(-1-day) / self.stockdayline['buy'] - 1
            self.stockdayline['close/buy{}'.format(day)] = self.stockdayline['close'].shift(-1-day) / self.stockdayline['buy'] - 1
        
        
        #day1
        self.stockdayline.loc[self.stockdayline['high/buy1'] >= stopgain,'yz']  = stopgain
        self.stockdayline.loc[(self.stockdayline['yz'] == 'tobeyz') & (self.stockdayline['close/buy1'] <= stoploss),'yz'] = self.stockdayline['close/buy1']
        
        #middle
        for day in range(2,holdday):
            self.stockdayline.loc[(self.stockdayline['yz'] == 'tobeyz') & (self.stockdayline['high/buy{}'.format(day)] >= stopgain),'yz'] = stopgain
            self.stockdayline.loc[(self.stockdayline['yz'] == 'tobeyz') & (self.stockdayline['close/buy{}'.format(day)] <= stoploss),'yz'] = self.stockdayline['close/buy{}'.format(day)]
           
        
        #lastday
        self.stockdayline.loc[(self.stockdayline['yz'] == 'tobeyz') & (self.stockdayline['high/buy3'] >= stopgain),'yz'] = stopgain
        self.stockdayline.loc[self.stockdayline['yz'] == 'tobeyz','yz']  = self.stockdayline['close/buy3']

    def std(self):
        #
        tmpma = self.stockdayline[['5dma','10dma','20dma']]
        tmpmastd = tmpma.std(axis=1)
        tmpmastd.name='mastd'
        self.stockdayline=self.stockdayline.join(tmpmastd)
        self.stockdayline['13dmastdma'] = self.stockdayline['mastd'].rolling(center=False,window=13).mean()
        self.stockdayline['mastdyz']=self.stockdayline['13dmastdma'].expanding(min_periods=1).min()
        
    def yycsy(self):
        #一阳串三阴,三均线进攻排列,第二天买入
        self.stockdayline['yycsy'] = True
        self.stockdayline['yycsy'] &= (self.stockdayline['5dma'] > self.stockdayline['open'])
        self.stockdayline['yycsy'] &= (self.stockdayline['10dma'] > self.stockdayline['open'])
        self.stockdayline['yycsy'] &= (self.stockdayline['20dma'] > self.stockdayline['open'])
        self.stockdayline['yycsy'] &= (self.stockdayline['5dma'] < self.stockdayline['close'])
        self.stockdayline['yycsy'] &= (self.stockdayline['10dma'] < self.stockdayline['close'])
        self.stockdayline['yycsy'] &= (self.stockdayline['20dma'] < self.stockdayline['close'])
        self.stockdayline['yycsy'] &= (self.stockdayline['5dma'] > self.stockdayline['10dma'])
        self.stockdayline['yycsy'] &= (self.stockdayline['10dma'] > self.stockdayline['20dma'])
        self.stockdayline['yycsy'] &= (self.stockdayline['mastdyz'] == self.stockdayline['13dmastdma'])


stopgains=[0.05,0.06,0.07,0.08,0.09,0.10,0.11,0.12,0.13,0.14,0.15]
stoplosses=[-0.02,-0.03,-0.04,-0.05]
holddays=[3,4,5,6,7,8,9,10]


def main():
    file = open('log.log','w')
    for code in depickle_stock_list():
        for stopgain in stopgains:
            for stoploss in stoplosses:
                for holdday in holddays:
                    try:
                        a=marun(code,stopgain,stoploss,holdday)
                        a.yycsy()
                        b=a.stockdayline[a.stockdayline['yycsy']==True]['yz']
                        c=b+1
                        c=c.cumprod()
                        file.write(code+','+str(stopgain)+','+str(stoploss)+','+str(holdday)+','+'{:.5f}'.format(c[-1:][0])+','+'{:.5f}'.format(b[b>0].count()/b.count())+','+'{:.5f}'.format(b.std())+'\n')
                    except Exception as e:
                        pass
    file.close()

def main2():
    file2 = open('allcodedays2.log','w')
    for code in depickle_stock_list():
        try:
            a=marun(code)
            a.yycsy()
            b=a.stockdayline[a.stockdayline['yycsy']==True]['yz']
            file2.write(code+'\n'+str(b)+'\n\n')
        except:
            pass
    file2.close()
    
def main3():
    file2 = open('out.log','w')
    today = '2016-10-31 00:00:00'#2016-10-25'
    for code in depickle_stock_list():
        try:
            a=marun(code)
            a.yycsy()
            b=a.stockdayline[a.stockdayline['yycsy']==True]['yz']
            if (str(b[-1:].index[0])) == today:
                file2.write(code+'\n')
        except:
            pass
    file2.close()
    
main2()