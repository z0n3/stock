

def teststrategy(data,stopgain=0.05,stoploss=-0.02,holdday=3):
    '''
    至少包含以下字段
    ['date','open','high','close','low','vol','amount','yz']
    返回止盈上损持有天数的收益结果
    '''
    #设置盈亏
    data['buy']=data['open'].shift(-1)
    data['gainorloss'] = 'tobeyz'
        
    for day in range(1,holdday+1):
        data['high/buy{}'.format(day)] = data['high'].shift(-1-day) / data['buy'] - 1
        data['close/buy{}'.format(day)] = data['close'].shift(-1-day) / data['buy'] - 1
        
        
    #day1
    data.loc[data['high/buy1'] >= stopgain,'gainorloss']  = stopgain
    data.loc[(data['gainorloss'] == 'tobeyz') & (data['close/buy1'] <= stoploss),'gainorloss'] = data['close/buy1']
    
    #middle
    for day in range(2,holdday):
        data.loc[(data['gainorloss'] == 'tobeyz') & (data['high/buy{}'.format(day)] >= stopgain),'gainorloss'] = stopgain
        data.loc[(data['gainorloss'] == 'tobeyz') & (data['close/buy{}'.format(day)] <= stoploss),'gainorloss'] = data['close/buy{}'.format(day)]
       
    
    #lastday
    data.loc[(data['gainorloss'] == 'tobeyz') & (data['high/buy3'] >= stopgain),'gainorloss'] = stopgain
    data.loc[data['gainorloss'] == 'tobeyz','gainorloss']  = data['close/buy3']

    return(data[data['yz']==True]['gainorloss'])
    
def holdgainloss(data,holdday=20):
    data['holdmaxgain'] = data['high'].shift(-holdday).rolling(center=False,window=holdday).max() / data['open'].shift(-1) - 1
    data['holdmaxloss'] = data['low'].shift(-holdday).rolling(center=False,window=holdday).min() / data['open'].shift(-1) - 1
    return(data[data['yz']==True][['holdmaxgain','holdmaxloss','downif','upif']])