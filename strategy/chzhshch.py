import sys
sys.path.append("..")
from core import Stock30
from core import depickle_stock_list
from core import get_stock_market



#temp
stocklist = ['600482']

class chzhshch(Stock30):
    '''
    descript
    '''
    def __init__(self,code):
        Stock30.__init__(self,code)
        Stock30.getline(self,code)
        self.ma(5)
        self.ma(10)
        self.macd(12,26,9)
        self.fzline={'low':list(reversed(list(self.stockdayline['low']))),'macd':list(reversed(list(self.stockdayline['macd']))),'macd_dea':list(reversed(list(self.stockdayline['macd_dea'])))}
    
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
        if i2 - i1 < 5:
            return False
        if i3 - i2 < 5:
            return False
        
        if min(self.fzline['low'][0:i1]) >= min(self.fzline['low'][i2:i3]):
            return False
        
        if sum(self.fzline['macd'][1:i1]) * 2 <= sum(self.fzline['macd'][i2:i3]):
            return False
        
        return True
                
        
        
def runchzhshch(logfile):
    #strtoday = datetime.datetime.now().strftime('%Y%m%d')
    #today = pd.Timestamp(strtoday)
    print('chzhshch output' + ':\n')
    logfile.write('chzhshch output' + ':\n')
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
    logfile.close()


if __name__ == "__main__":
    logfile=open('chzhshch.log','w')
    runchzhshch(logfile)