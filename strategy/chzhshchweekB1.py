import sys
sys.path.append("..")
from core import StockW
from core import depickle_stock_list
from core import get_stock_market



#temp
stocklist = ['600389']

class jasonshort(StockW):
    '''
    depend week line 
    '''
    def __init__(self,code,trading):
        StockW.__init__(self,code)
        StockW.getline(self,code)
        if trading:
            self.stockdayline = self.stockdayline[:-1]
        self.macd(12,26,9)
        #self.stockdayline.to_csv('a.csv')
        self.fzline={'low':list(reversed(list(self.stockdayline['low']))),'macd':list(reversed(list(self.stockdayline['macd']))),'open':list(reversed(list(self.stockdayline['open']))),'close':list(reversed(list(self.stockdayline['close'])))}
    
    def test(self):
        if self.fzline['macd'][0] >= 0:
            return False
        if self.fzline['macd'][1] >= 0:
            return False
        if self.fzline['macd'][2] >= 0:
            return False
        if self.fzline['macd'][0] <= self.fzline['macd'][1]:
            return False
        if self.fzline['macd'][1] >= self.fzline['macd'][2]:
            return False
        if self.fzline['low'][0] <= self.fzline['low'][1]:
            return False
        if self.fzline['low'][1] >= self.fzline['low'][2]:
            return False
        if self.fzline['close'][1] >= self.fzline['open'][1]:
            return False        
            
        i = 0
        while(self.fzline['macd'][i] < 0):
            i=i+1
        i1 = i
        while(self.fzline['macd'][i] > 0):
            i=i+1
        i2 = i
        while(self.fzline['macd'][i] < 0):
            i=i+1
        i3 = i
        #print(i1,i2,i3)
        if i2 - i1 <= 3:
            return False
        if i3 - i2 <= 5:
            return False
        
        #if self.fzline['low'][1] >= min(self.fzline['low'][i1:i3]):
        #    return False
        
        if sum(self.fzline['macd'][1:i1]) * 2 <= sum(self.fzline['macd'][i2:i3]):
            return False
        return True
                
        
        
def runchzhshchweekB1(logfile,trading):
    #strtoday = datetime.datetime.now().strftime('%Y%m%d')
    #today = pd.Timestamp(strtoday)

    print('chzhshch_week_B1 output' + ':\n')
    logfile.write('chzhshch_week_B1 output' + ':\n')
    for code in depickle_stock_list():
        if get_stock_market(code) in ['sh','sz']:
            try:
                a=jasonshort(code,trading)
                out = a.test()
                if out:
                    print(code)
                    logfile.write(code+'\n')

            except Exception as e:
                print(e)



if __name__ == "__main__":
    logfile=open('chzhshch.log','w')
    runchzhshchweekB1(logfile,True)        
    logfile.close()