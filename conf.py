stock_list_pkl_file = '../data/temp/stocklist.pkl'
stock_day_line_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/'\
                  'vMS_FuQuanMarketHistory/stockid/{}.phtml?year={}&jidu={}'

stock_day_line_headers = ['date','open','high','close','low','vol','amount','factor','non']
stock_day_line_file = '../data/perm/dayline/'
stock_oneday_line_file = '../data/temp/'