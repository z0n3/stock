#import struct
from StockClass import Stock
from datetime import datetime
import sys
sys.path.append("..")
from conf import tdx_fz_line_file
from core import depickle_stock_list
from core import get_stock_market

generaldir = tdx_fz_line_file   #new_zx_allin1
Sse_lday = generaldir + r"\sh\lday\sh"
Sze_lday = generaldir + r"\sz\lday\sz"


def minchoice(logfile):
    print('minchoice output' + ':\n')
    logfile.write('minchoice output' + ':\n')
    for code in depickle_stock_list():
        #print(code)
        market = get_stock_market(code)
        if market in ['sh','sz']:
            try:
                if market == 'sh':
                    choosedir = Sse_lday
                else:
                    choosedir = Sze_lday
                    
                stk=Stock(code)
                stk.readldaysim(choosedir,20)
                #print(stk.ldayvalue)
                upcount = 0
                for n in range(15):
                    if stk.limitup( n ): upcount += 1
                #print(upcount)
                if upcount >= 3:
                    
                    gd = stk.gaodian(0,14)
                    #print(stk.ldayvalue[0]["Close"] / gd)
                    if stk.ldayvalue[0]["Close"] / gd < 0.85:
                        
                        print(code)
                        logfile.write(code+'\n')
    
            except Exception as e:
                pass#print(e)

if __name__ == "__main__":
    strtoday = datetime.now().strftime('%Y%m%d')
    logfile = open('{}_minchoice.log'.format(strtoday),'w')
    minchoice(logfile)        
    logfile.close()
