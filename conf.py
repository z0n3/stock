stock_list_pkl_file = '../data/temp/stocklist.pkl'
stock_day_line_url = 'http://vip.stock.finance.sina.com.cn/corp/go.php/'\
                  'vMS_FuQuanMarketHistory/stockid/{}.phtml?year={}&jidu={}'

stock_day_line_headers = ['date','open','high','close','low','vol','amount','factor','non']
stock_fz_line_headers = ['datetime','open','high','low','close','amount','vol','non']
stock_day_line_file = '../data/perm/dayline/'
stock_fz_line_file = '../data/perm/fzline/'
#tdx_fz_line_file = r'D:\zd_pazq\vipdoc'
tdx_fz_line_file = r'C:\new_gxzq_v6.56'
stock_oneday_line_file = '../data/temp/'