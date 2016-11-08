import matplotlib.pyplot as plt
import sys
sys.path.append("..")
from core import Stock
from core import depickle_stock_list

#todo:
#增加趋势的分析



#temp
stocklist = ['601218','601933']

class mastd(Stock):
    '''
    backtest base at the sell day
    descript
    '''
    def __init__(self,code,stopgain=0.05,stoploss=-0.02,holdday=3):
        Stock.__init__(self,code)
        self.ma(5)
        self.ma(10)
        self.ma(20)
        self.volma(20)
        #self.cut2006()
        #验证数据
        
    def cut2006(self):
        self.stockdayline = self.stockdayline[self.stockdayline.index>'2006-01-01']
        
    def std(self):
        #
        tmpma = self.stockdayline[['5dma','10dma','20dma']]
        tmpmastd = tmpma.std(axis=1)
        tmpmastd.name='mastd'
        self.stockdayline=self.stockdayline.join(tmpmastd)
        self.stockdayline['13dmastdma'] = self.stockdayline['mastd'].rolling(center=False,window=13).mean()
        self.stockdayline['60dmax']=self.stockdayline['close'].shift(-60).rolling(center=False,window=60).max()
        self.stockdayline['revmastd']=self.stockdayline['60dmax'] / self.stockdayline['open'].shift(-1) - 1
        
        self.stockdayline['mastdyz'] = self.stockdayline['13dmastdma'] / self.stockdayline['13dmastdma'].expanding(min_periods=1).min()
        #print(tmpma)


def main():
    file = open('mastd.log','w')
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    for code in depickle_stock_list():
        try:
            a=mastd(code)
            a.std()
            rate = a.stockdayline['mastdyz'][-20:].min()
            if a.stockdayline['close'].count() > 5*250:
                #if rate < 1.05:
                    #plt绘图
                    ax1.plot(a.stockdayline.index,a.stockdayline['close'],color="red")
                    ax2.plot(a.stockdayline.index,a.stockdayline['13dmastdma'],color="blue")
                    ax2.set_ylim([0, 3*a.stockdayline['13dmastdma'].min()])
                    plt.savefig('.\png\{}.png'.format(code), dpi=120)
                    ax1.cla()
                    ax2.cla()
                    file.write(str(code) + ',' + '{:.5f}'.format(rate) + '\n')
        except:
            pass
    file.close()
    
a=mastd('600160')
#a.std()
#print(a.stockdayline['mastdyz'][-20:].min())
#print(a.stockdayline[['mastdyz','13dmastdma']].to_csv('a.csv'))
#a.stockdayline[['close','13dmastdma']].plot(subplots=True)
    
#main()
    
    
'''
在单y轴制图中
import matplotlib.pylab as plt # 导入绘图包
plt.figure() # 创建图像文件
plt.plot(...)  # 绘制图像
plt.show() # 显示图像

在双y轴制图中，绘图命令和以往不同，因而在此记录以备日后查阅。以一段程序为例
fig, ax1 = plt.subplots()  # 使用subplots()创建窗口
ax2 = ax1.twinx() # 创建第二个坐标轴
ax1.plot(pos_z, E_z, linewidth = 2)  # E_z是一组数据，不用在意
ax2.plot(pos_z, Enhance_z, linewidth = 3) # Ehance_z 是一组数据，不用在意
ax1.set_xlabel('position (nm)', fontsize = 16)  # fontsize使用方法和plt.xlabel()中一样
ax1.set_ylabel('|$E_{z}$| (V/m)', fontsize = 16)
ax2.set_ylabel('Enhancement', fontsize = 16)
ax1.set_xlim([0, max(pos_z)]) # 设置坐标轴范围的语句有所变化
ax1.set_ylim(0, max(E_z))
ax2.set_ylim([0, max(Enhance_z)])
plt.show()
'''