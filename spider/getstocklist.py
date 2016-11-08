import re
import requests
import pickle
import sys
sys.path.append("..")
from conf import stock_list_pkl_file



def getstocklist():
    stock_list_url = 'http://www.shdjt.com/js/lib/astock.js'
    
    req = requests.get(stock_list_url)
    grep_req = re.compile('~(\d+)`(.*?)`')
    stock_list_tmp = grep_req.findall(req.text)
    
    stock_list = {}
    for t in stock_list_tmp:
        stock_list[t[0]] = t[1]
    #循环待简化
    
    stock_list_pkl = open(stock_list_pkl_file,'wb')
    pickle.dump(stock_list,stock_list_pkl)
    stock_list_pkl.close()
    
    #print(stock_list)