import struct
import os
import time
import sys
sys.path.append("..")
from core import get_stock_market
from conf import stock_fz_line_file
from conf import tdx_fz_line_file
from core import depickle_stock_list

Daylength = 32 # one day data is 32 byte.


def getstockfzline(stocklist):
    '''
    读取通达信5分钟数据
    '''
    for root, dirs, files in os.walk(stock_fz_line_file):
        for file in files:
            os.remove(root+file)
    time.sleep(3)
    for code in (stocklist):
        prefix = get_stock_market(code)
        if prefix in ['sh','sz']: 
            try:
                file_to_w = stock_fz_line_file + prefix + code + '.csv'
                file_to_o = tdx_fz_line_file + '/' + prefix + '/fzline' + '/' + prefix + code + '.lc5'
                file_o = open ( file_to_o, "rb" )
                file_w = open ( file_to_w, "w" )
                count = 0
                while( file_o.seek( -(count + 1) * Daylength, 2 ) ):
                    tmpfz = struct.unpack('hhfffffii', file_o.read(32))
                    tmpdata = []
                    tmpdata.append('{}-{}-{} {:0>2}:{:0>2}:00'.format(tmpfz[0]//2048+2004,tmpfz[0]%2048//100,tmpfz[0]%2048%100,tmpfz[1]//60,tmpfz[1]%60))
                    tmpdata.append('{:.2f}'.format(tmpfz[2]))   #open
                    tmpdata.append('{:.2f}'.format(tmpfz[3]))   #high
                    tmpdata.append('{:.2f}'.format(tmpfz[4]))   #low
                    tmpdata.append('{:.2f}'.format(tmpfz[5]))   #close
                    tmpdata.append('{:.2f}'.format(tmpfz[6]))   #amount
                    tmpdata.append('{:.2f}'.format(tmpfz[7]))   #vol
                    
                    for d in tmpdata:
                        file_w.write(d)
                        file_w.write(',')
                    file_w.write('\n')
                    #print(tmpdata)
        
                    count += 1
                    #if count > 187:break
                file_o.close()
                file_w.close()
            except:
                pass


if __name__ == "__main__":
    getstockfzline(depickle_stock_list())
