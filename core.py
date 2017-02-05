import pickle
import struct
import pandas as pd
import sys
sys.path.append("..")
from conf import stock_day_line_file
from conf import stock_day_line_headers
from conf import stock_fz_line_file
from conf import stock_fz_line_headers
from conf import stock_list_pkl_file
from conf import tdx_fz_line_file

def depickle_stock_list():
    stock_list_pkl = open(stock_list_pkl_file,'rb')
    return(pickle.load(stock_list_pkl))

def get_stock_market(code):
    '''
    code is str type.
    '''
    if code.startswith(('600','601','603')):
        return('sh')
    #elif code.startswith(('000','002','300')):
    elif code.startswith(('000','002')):
        return('sz')
    else:
        return('other')


        


class Stock(object):
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

    def drop(self):
        self.stockdayline['upif'] = (self.stockdayline['high'] > self.stockdayline['high'].shift(1)) & (self.stockdayline['low'] > self.stockdayline['low'].shift(1))
        self.stockdayline['dropif'] = (self.stockdayline['high'] < self.stockdayline['high'].shift(1)) & (self.stockdayline['low'] > self.stockdayline['low'].shift(1))
        dropcount = self.stockdayline[self.stockdayline['dropif']==True]['dropif'].count()
        self.stockdayline.loc[(self.stockdayline['dropif'].shift(-1)==True) & (self.stockdayline['upif']==True),'low']  = self.stockdayline['low'].shift(-1)
        self.stockdayline.loc[(self.stockdayline['dropif'].shift(-1)==True) & (self.stockdayline['upif']==False),'high']  = self.stockdayline['high'].shift(-1)
        self.stockdayline = self.stockdayline[self.stockdayline['dropif']==False]
        del self.stockdayline['upif']
        del self.stockdayline['dropif']

        return dropcount
    
    def markgd(self):
        pass
        
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
        
class Stockfz(Stock):
    '''
    5分钟数据
    init: Stock('600000')
    '''
    def __init__(self,code):
        Stock.__init__(self,code)
    
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
'''
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
'''        
        
class Stock30(Stock):
    '''
    30分钟数据
    init: Stock('600000')
    '''
    def __init__(self,code):
        Stock.__init__(self,code)
    
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
        #5minto30min
        ohlc_dict = {'open':'first','high':'max','low':'min','close':'last','amount':'sum','vol':'sum'}
        data = data.resample('30Min',how=ohlc_dict,closed='right',label='right')
        data = data.dropna()
        self.stockdayline = data        
        
    def getline_tmp(self,code):
        prefix = get_stock_market(code)
        if prefix not in ['sh','sz']:
            #print('The stock is not tradeable.')
            return
        Daylength = 32 # one day data is 32 byte.
        try:
            file_to_o = tdx_fz_line_file + '/' + prefix + '/fzline' + '/' + prefix + code + '.lc5'
            file_o = open ( file_to_o, "rb" )
            count = 0
            tmpopen = []
            tmphigh = []
            tmplow = []
            tmpclose = []
            tmpamount = []
            tmpvol = []
            tmpdatetime = []
            while( file_o.seek( -(count + 1) * Daylength, 2 ) ):
                tmpfz = struct.unpack('hhfffffii', file_o.read(32))
                tmpdatetime.append('{}-{}-{} {:0>2}:{:0>2}:00'.format(tmpfz[0]//2048+2004,tmpfz[0]%2048//100,tmpfz[0]%2048%100,tmpfz[1]//60,tmpfz[1]%60))
                tmpopen.append('{:.2f}'.format(tmpfz[2]))   #open
                tmphigh.append('{:.2f}'.format(tmpfz[3]))   #high
                tmplow.append('{:.2f}'.format(tmpfz[4]))   #low
                tmpclose.append('{:.2f}'.format(tmpfz[5]))   #close
                #tmpamount.append('{:.2f}'.format(tmpfz[6]))   #amount
                tmpamount.append(tmpfz[6])   #amount
                tmpvol.append(tmpfz[7])   #vol
                

                #print(tmpopen)
    
                count += 1
            file_o.close()
        except Exception as e:
            return
            
        #print(tmpopen)    
        tmpdata = {'open':tmpopen,'high':tmphigh,'low':tmplow,'close':tmpclose,'amount':tmpamount,'vol':tmpvol}
        data = pd.DataFrame(tmpdata,index=tmpdatetime)
        #print(data.head())
        index_tmp = list(data.index)
        index_tmp.sort()
        data = data.reindex(index_tmp)
        data.index = pd.to_datetime(data.index)
        #print(data.head())
        #5minto30min
        ohlc_dict = {'open':'first','high':'max','low':'min','close':'last','amount':'sum','vol':'sum'}
        data = data.resample('30Min',how=ohlc_dict,closed='right',label='right')
        data = data.dropna()
        #print(data.head())
        self.stockdayline = data               
        
        
        
        
        
        
        
        
        
        
        
        