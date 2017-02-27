import sys
sys.path.append("..")
from core import StockW
from core import depickle_stock_list
from core import get_stock_market

def testlow(d0,d1,d2,d3,d4):
    if d2<d1:
        if d2<d0:
            if d2<d3:
                if d2<d4:
                    if d1<d0:
                        if d3<d4:
                            return True

#temp
stocklist = ['000965']

class jasonlong(StockW):
    '''
    depend W line 
    '''
    def __init__(self,code,trading):
        StockW.__init__(self,code)
        StockW.getline(self,code)
        if trading:
            self.stockdayline = self.stockdayline[:-1]
        #self.stockdayline.to_csv('a.csv')
        self.macd(12,26,9)
        self.wline={'low':list(reversed(list(self.stockdayline['low']))),'macd':list(reversed(list(self.stockdayline['macd']))),'open':list(reversed(list(self.stockdayline['open']))),'close':list(reversed(list(self.stockdayline['close']))),'macd_dif':list(reversed(list(self.stockdayline['macd_dif'])))}
        #self.code = code
        #self.stockdayline.to_csv('a.csv')
    def test(self):
        if self.wline['macd'][0] <= 0:
            return False
        if self.wline['macd'][1] > 0:
            return False
        i=0
        while True:
            if(self.wline['macd'][i] > 0) & (self.wline['macd'][i+1] > 0):
                break
            i=i+1
        if i < 11:
            return False
        if self.wline['macd_dif'][1] > self.wline['macd_dif'][i]:
            return False
        
        lowlist=[]
        for j in range(i-2):
            if testlow(self.wline['macd'][j-2],self.wline['macd'][j-1],self.wline['macd'][j],self.wline['macd'][j+1],self.wline['macd'][j+2]):
                lowlist.append(j)
                
        if len(lowlist) == 1:
            return False
        
        if min(self.wline['close'][lowlist[0]:lowlist[1]]) < min(self.wline['close'][lowlist[-1]:i]):
            return False
            

        return True     
        
        
def runjasonlong(logfile,trading):
    #strtoday = datetime.datetime.now().strftime('%Y%m%d')
    #today = pd.Timestamp(strtoday)

    print('chzhshch_w_jasonlong output' + ':\n')
    logfile.write('chzhshch_w_jasonlong output' + ':\n')
    for code in depickle_stock_list():
        if get_stock_market(code) in ['sh','sz']:
            try:
                a=jasonlong(code,trading)
                #print(a.stockdayline)
                out = a.test()
                if out:
                    print(code)
                    logfile.write(code+'\n')

            except Exception as e:
                pass # print(e)



if __name__ == "__main__":
    logfile=open('chzhshch.log','w')
    runjasonlong(logfile,False)        
    logfile.close()