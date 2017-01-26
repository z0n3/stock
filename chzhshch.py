import sys
sys.path.append("..")
from core import Stock
from core import depickle_stock_list
from core import get_stock_market



#temp
stocklist = ['600482']

class chzhshch(Stock):
    '''
    descript
    '''
    def __init__(self,code):
        Stock.__init__(self,code)
        Stock.getline(self,code)
        #self.ma(5)
        #self.ma(10)
        #self.macd(12,26,9)
        while(self.drop() > 0):
            pass
        
        tmpstockdayline = self.stockdayline[-3:]
        self.threeline={'low':list(reversed(list(tmpstockdayline['low'])))}
        #print(self.threeline)


        #self.stockdayline_drop.to_csv('a.csv')
        #self.stockdayline.to_csv('b.csv')
    
    def test(self):
        if ((self.threeline[0] > self.threeline[1]) & (self.threeline[2] > self.threeline[1])):
            return True
        else:
            return False

                
        
        
def runchzhshch(logfile):
    #strtoday = datetime.datetime.now().strftime('%Y%m%d')
    #today = pd.Timestamp(strtoday)
    print('chzhshch_new output' + ':\n')
    logfile.write('chzhshch_new output' + ':\n')
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
    logfile=open('chzhshch_new.log','w')
    runchzhshch(logfile)
    logfile.close()