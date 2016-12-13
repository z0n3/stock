import pickle
import pandas as pd
import sys
sys.path.append("..")
from conf import stock_day_line_file
from conf import stock_day_line_headers
from conf import stock_fz_line_file
from conf import stock_fz_line_headers
from conf import stock_list_pkl_file

def depickle_stock_list():
    stock_list_pkl = open(stock_list_pkl_file,'rb')
    return(pickle.load(stock_list_pkl))

def get_stock_market(code):
    '''
    code is str type.
    '''
    if code.startswith(('600','601','603')):
        return('sh')
    elif code.startswith(('000','002','300')):
        return('sz')
    else:
        return('other')


        


class Stock(object):
    '''
    Stock class
    init: Stock('600000')
    '''
    def __init__(self,code):
        prefix = get_stock_market(code)
        if prefix not in ['sh','sz']:
            #print('The stock is not tradeable.')
            return
        file_open = stock_day_line_file + prefix + code + '.csv'
        data = pd.read_csv(file_open, header=None, sep = ',', names = stock_day_line_headers, index_col = 0)
        del data['non']
        del data['factor']
        data = data.set_index(pd.to_datetime(data.index))
        
        index_tmp = list(data.index)
        index_tmp.sort()
        data = data.reindex(index_tmp)
        self.stockdayline = data
        self.stockdayline['percent'] = self.stockdayline['close'] / self.stockdayline['close'].shift(1) - 1

    
    def openrev(self):
        '''
        base the sell day
        sell day open - buy day open - 0.5%fee
        '''
        self.stockdayline['openrev'] = (self.stockdayline['open'] / self.stockdayline['open'].shift(1) - 1.005)
        
    def ma(self,days):
        self.stockdayline[str(days)+'dma'] = self.stockdayline['close'].rolling(center=False,window=days).mean()

    def volma(self,days):
        self.stockdayline[str(days)+'volma'] = self.stockdayline['vol'].rolling(center=False,window=days).mean()
        
    def ema(self,days):
        self.stockdayline[str(days)+'ema'] = self.stockdayline['close'].ewm(ignore_na=False,min_periods=0,adjust=False,span=days).mean()
    
    def macd(self,short,long,mid):
        self.ema(short)
        self.ema(long)
        self.stockdayline['macd_dif'] = self.stockdayline[str(short)+'ema'] - self.stockdayline[str(long)+'ema']
        self.stockdayline['macd_dea'] = self.stockdayline['macd_dif'].ewm(ignore_na=False,min_periods=0,adjust=False,span=mid).mean()
        self.stockdayline['macd'] = 2 * (self.stockdayline['macd_dif'] - self.stockdayline['macd_dea'])
        del self.stockdayline[str(short)+'ema']   
        del self.stockdayline[str(long)+'ema']
        
    def deepup(self):
        self.stockdayline['deepup'] = (self.stockdayline['percent'] >= 0.07)
        
    def midup(self):
        self.stockdayline['midup'] = ((0.03 <= self.stockdayline['percent'] )
                                    & (self.stockdayline['percent'] < 0.07))
                                    
    def shallowup(self):
        self.stockdayline['shallowup'] = ((0.03 > self.stockdayline['percent'] )
                                            & (self.stockdayline['percent'] > 0))
                
    def deepdown(self):
        self.stockdayline['deepdown'] = (self.stockdayline['percent'] <= -0.07)
        
    def middown(self):
        self.stockdayline['middown'] = ((-0.03 >= self.stockdayline['percent'] )
                                            & (self.stockdayline['percent'] > -0.07))
                
    def shallowdown(self):
        self.stockdayline['shallowdown'] = ((-0.03 < self.stockdayline['percent'] )
                                            & (self.stockdayline['percent'] < 0))
    
    '''
    def ifup(self):
        percent = self.stockdayline['close'] / self.stockdayline['close'].shift(1) - 1
        self.stockdayline['ifup'] = (percent > 0.0)
        
    def ifdown(self):
        percent = self.stockdayline['close'] / self.stockdayline['close'].shift(1) - 1
        self.stockdayline['ifup'] = (percent < 0.0)
    
    def ifshallow(self):
        percent = self.stockdayline['close'] / self.stockdayline['close'].shift(1) - 1
        self.stockdayline['ifshallow'] = (0.03 > abs(percent))
    '''        
        
class Stockfz(object):
    '''
    Stock class
    init: Stock('600000')
    '''
    def __init__(self,code):
        pass
    
    def getline(self,code):
        prefix = get_stock_market(code)
        if prefix not in ['sh','sz']:
            #print('The stock is not tradeable.')
            return
        file_open = stock_fz_line_file + prefix + code + '.csv'
        data = pd.read_csv(file_open, header=None, sep = ',', names = stock_fz_line_headers, index_col = 0)
        del data['non']
        data = data.set_index(pd.to_datetime(data.index))
        
        index_tmp = list(data.index)
        index_tmp.sort()
        data = data.reindex(index_tmp)
        self.stockdayline = data

    def ma(self,days):
        self.stockdayline[str(days)+'dma'] = self.stockdayline['close'].rolling(center=False,window=days).mean()

    def volma(self,days):
        self.stockdayline[str(days)+'volma'] = self.stockdayline['vol'].rolling(center=False,window=days).mean()
        
    def ema(self,days):
        self.stockdayline[str(days)+'ema'] = self.stockdayline['close'].ewm(ignore_na=False,min_periods=0,adjust=False,span=days).mean()
    
    def macd(self,short,long,mid):
        self.ema(short)
        self.ema(long)
        self.stockdayline['macd_dif'] = self.stockdayline[str(short)+'ema'] - self.stockdayline[str(long)+'ema']
        self.stockdayline['macd_dea'] = self.stockdayline['macd_dif'].ewm(ignore_na=False,min_periods=0,adjust=False,span=mid).mean()
        self.stockdayline['macd'] = 2 * (self.stockdayline['macd_dif'] - self.stockdayline['macd_dea'])
        del self.stockdayline[str(short)+'ema']   
        del self.stockdayline[str(long)+'ema']        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        