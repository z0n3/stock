import sys
sys.path.append("..")
from core import Stock
from core import depickle_stock_list
from core import get_stock_market



#temp
stocklist = ['300419']

class chzhshch(Stock):
    '''
    descript
    '''
    def __init__(self,code):
        Stock.__init__(self,code)
        Stock.getline(self,code)
        self.ma(5)
        self.ma(10)
        self.macd(12,26,9)
        self.fzline={'low':list(reversed(list(self.stockdayline['low']))),'high':list(reversed(list(self.stockdayline['high']))),'macd':list(reversed(list(self.stockdayline['macd']))),'5dma':list(reversed(list(self.stockdayline['5dma']))),'10dma':list(reversed(list(self.stockdayline['10dma'])))}
    
    def test(self):
        if self.fzline['macd'][0] <= 0:
            return False
        if self.fzline['macd'][1] <= 0:
            return False
        if self.fzline['macd'][2] <= 0:
            return False
        if self.fzline['macd'][0] >= self.fzline['macd'][1]:
            return False
        if self.fzline['macd'][1] >= self.fzline['macd'][2]:
            return False
        
        if self.fzline['5dma'][0] >= self.fzline['5dma'][1]:
            return False
            
        i = 0
        if self.fzline['5dma'][i] > self.fzline['10dma'][i]:
            while (self.fzline['5dma'][i] - self.fzline['10dma'][i])*(self.fzline['5dma'][i+1] - self.fzline['10dma'][i+1])>0:
                i=i+1
            i=i+1
        while (self.fzline['5dma'][i] - self.fzline['10dma'][i])*(self.fzline['5dma'][i+1] - self.fzline['10dma'][i+1])>0:
            i=i+1
        cross1 = i
        i=i+1        
        while (self.fzline['5dma'][i] - self.fzline['10dma'][i])*(self.fzline['5dma'][i+1] - self.fzline['10dma'][i+1])>0:
            i=i+1
        #cross2 = i
        i=i+1
        while (self.fzline['5dma'][i] - self.fzline['10dma'][i])*(self.fzline['5dma'][i+1] - self.fzline['10dma'][i+1])>0:
            i=i+1
        #cross3 = i
        i=i+1        
        while (self.fzline['5dma'][i] - self.fzline['10dma'][i])*(self.fzline['5dma'][i+1] - self.fzline['10dma'][i+1])>0:
            i=i+1
        cross4 = i
        #i=i+1        
        #while (self.fzline['5dma'][i] - self.fzline['10dma'][i])*(self.fzline['5dma'][i+1] - self.fzline['10dma'][i+1])>0:
        #    i=i+1
        #cross5 = i
        #if cross4 < 20:
        #    return False
        if max(self.fzline['high'][cross1:(cross4+5)]) >= self.fzline['low'][0]:
            return False
        if self.fzline['5dma'][cross4] <= self.fzline['5dma'][cross1]:
            return False
        return True
                
        
        
def runchzhshch(logfile):
    #strtoday = datetime.datetime.now().strftime('%Y%m%d')
    #today = pd.Timestamp(strtoday)
    print('chzhshch_day_B3 output' + ':\n')
    logfile.write('chzhshch_day_B3 output' + ':\n')
    for code in depickle_stock_list():
        if get_stock_market(code) in ['sh','sz']:
            try:
                a=chzhshch(code)
                out = a.test()
                if out:
                    print(code)
                    logfile.write(code+'\n')

            except Exception as e:
                pass
    #logfile.close()


if __name__ == "__main__":
    logfile=open('chzhshch.log','w')
    runchzhshch(logfile)