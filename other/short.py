import core
import pylab as pl


stock = core.Stock('000001')
shdir = r'D:\zd_pazq\vipdoc\sh\lday\sh'
szdir = r'D:\zd_pazq\vipdoc\sz\lday\sz'
stock.readldayclose(szdir)
#print(type(stock.ldayvalue))
#print(stock.ldayvalue[-1])

numbers = len(stock.ldayvalue)
for x in range(numbers):
    stock.ldayvalue[x]['num'] = (numbers -1 - x)
    
level1 = []
level2 = []
level3 = []
def isharami ( today, yesterday ):  #删除孕线及反孕线function
    if (today['High'] - yesterday['High']) * (today['Low'] - yesterday['Low']) <= 0:
        return True
    else:
        return False

afterharami = stock.ldayvalue.copy()
    
for x in range(1,numbers): #删除孕线及反孕线
    try:
        if isharami(afterharami[x], afterharami[x+1]):
            del afterharami[x]
    except:
        pass
    
def filtervalue ( value, level ):
    tmp = []
    tmp.append(value[0])

#    print(len(value))
    for num in range(level,len(value)-level):
        if (value[num-level]['High'] < value[num]['High'] > value[num+level]['High']):
            tmp.append(value[num])
        elif (value[num-level]['Low'] > value[num]['Low'] < value[num+level]['Low']):
            tmp.append(value[num])
    return tmp

level1 = filtervalue( afterharami, 1 )
level2 = filtervalue( level1, 2 )
level3 = filtervalue( level2, 3 )

for x in stock.ldayvalue[:100]: print(x)
print('*'*10)
for x in level1[:100]: print(x)
print('*1'*10)
for x in level2[:100]: print(x)
print('*2'*10)
for x in level3: print(x)
print('*3'*10)
print(len(level1),len(level2),len(level3))


pl.plot([x['num'] for x in stock.ldayvalue],[y['High'] for y in stock.ldayvalue],'k')
pl.plot([x['num'] for x in level1],[y['High'] for y in level1],'r')
#pl.plot([x['num'] for x in level2],[y['High'] for y in level2],'y')
#pl.plot([x['num'] for x in level3],[y['High'] for y in level3],'b')
pl.show()
#print([int(x['Date']) for x in level1])







