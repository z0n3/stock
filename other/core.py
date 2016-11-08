import struct

Daylength = 32 # one day data is 32 byte.

class Market:
    '''
    '''
    def __init__ ( self ):
        self.codelist = {}
        self.block_gn = {}
        
    def initcodelist ( self, choosedir ):
        fp = open ( choosedir, "rb" )
        fp.read(50)
        c = 0
        while (fp.seek((50+c*314),0)):
            c += 1
            code = fp.read(6).decode('GBK')
            if not(code):
                break
            fp.read(17)
            codename = fp.read(8)
            for nc in range(8):
                if codename[nc] == 0:
                    codename = codename[:nc]
                    break
            codename = codename.decode('GBK')
            self.codelist[code] = codename
        fp.close()

    def initblock_gn ( self, choosedir ):
        fp = open ( choosedir, "rb" )
        fp.seek( 0, 0 )
        fp.read(384)
        block_gn_c = struct.unpack("h", fp.read(2))[0]
#        print(block_gn_c)
        for c in range(block_gn_c):
            fp.seek( (386 + c*2813), 0 )
            block_gn_name = fp.read(9)
            for nc in range(9):
                if block_gn_name[nc] == 0:
                    block_gn_name = block_gn_name[:nc]
                    break
            block_gn_name = block_gn_name.decode('GBK')
#            print(block_gn_name)
            block_gn_dc = struct.unpack("h", fp.read(2))[0]
#            print(block_gn_dc)
            fp.read(2)
            block_gn_l = []
            for x in range(block_gn_dc):
                block_gn_l.append(fp.read(6).decode('GBK'))
                fp.read(1)
            self.block_gn[block_gn_name]=block_gn_l
        fp.close()

    def initblock_hy ( self, choosedirhy, choosedirzs ):
        fphy = open ( choosedirhy, "r" )
        hyout = fphy.readlines()
        fphy.close()
        fpzs = open ( choosedirzs, "r" )
        while True:
            zs = fpzs.readline()
            if not zs:
                break
            zs = zs.split('|')
            if zs[2] == '2': #行业数据标签
                if len(zs[5]) >= 5:
                    if zs[5][5] != '0': #一级行业数据
                        if zs[0][:3] != 'TDX':
                            hylist = []
                            for s in hyout:
                                s = s.split('|')
                                if s[2][:5] == zs[5][:5]:
                                    hylist.append(s[1])
                            self.block_gn[zs[0]] = hylist
        fpzs.close()
        
class Stock:
    '''
    [
    {'Low': 21.71, 'VOL': 1219100904, 'Date': 20141205, 'High': 23.18, 'Close': 23.18, 'Open': 22.47, 'AMO': 1355762841},
    {'Low': 19.02, 'VOL': 730966743, 'Date': 20141204, 'High': 21.07, 'Close': 21.07, 'Open': 19.14, 'AMO': 1348298197},
    {'Low': 18.38, 'VOL': 840389639, 'Date': 20141203, 'High': 20.15, 'Close': 19.15, 'Open': 18.9, 'AMO': 1349673901}]
    '''
    def __init__ ( self, code ):
        self.code = code
        self.ldayvalue = []
        
    def readlday ( self, choosedir ):
        fp = open ( choosedir + self.code + ".day", "rb" )
        count = 0
        while( fp.seek( -(count + 1) * Daylength, 2 ) ):
            tmplday = {}
            tmplday["Date"] = struct.unpack("i", fp.read(4))[0]
            tmplday["Open"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["High"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["Low"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["Close"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["AMO"] = struct.unpack("f", fp.read(4))[0]
            tmplday["VOL"] = struct.unpack("i", fp.read(4))[0]
            self.ldayvalue.append(tmplday)
            count += 1
        fp.seek( 0, 0 )         #读取历史第一天的数据
        tmplday = {}
        tmplday["Date"] = struct.unpack("i", fp.read(4))[0]
        tmplday["Open"] = struct.unpack("i", fp.read(4))[0] / 100
        tmplday["High"] = struct.unpack("i", fp.read(4))[0] / 100
        tmplday["Low"] = struct.unpack("i", fp.read(4))[0] / 100
        tmplday["Close"] = struct.unpack("i", fp.read(4))[0] / 100
        tmplday["AMO"] = struct.unpack("f", fp.read(4))[0]
        tmplday["VOL"] = struct.unpack("i", fp.read(4))[0]
        self.ldayvalue.append(tmplday)
        fp.close()

    def readldayclose ( self, choosedir ):
        fp = open ( choosedir + self.code + ".day", "rb" )
        count = 0
        while( fp.seek( -(count + 1) * Daylength, 2 ) ):
            tmplday = {}
            tmplday["Date"] = struct.unpack("i", fp.read(4))[0]
            fp.read(4)
            tmplday["High"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["Low"] = struct.unpack("i", fp.read(4))[0] / 100
            fp.read(12)
            self.ldayvalue.append(tmplday)
            count += 1
        fp.seek( 0, 0 )
        tmplday = {}
        tmplday["Date"] = struct.unpack("i", fp.read(4))[0]
        fp.read(4)
        tmplday["High"] = struct.unpack("i", fp.read(4))[0] / 100
        tmplday["Low"] = struct.unpack("i", fp.read(4))[0] / 100
        fp.read(12)
        self.ldayvalue.append(tmplday)
        fp.close()
        
                
    def readldaysim ( self, choosedir, n ):
        fp = open ( choosedir + self.code + ".day", "rb" )
        for x in range(n):
            fp.seek( -(x + 1) * Daylength, 2 )
            tmplday = {}
            tmplday["Date"] = struct.unpack("i", fp.read(4))[0]
            tmplday["Open"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["High"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["Low"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["Close"] = struct.unpack("i", fp.read(4))[0] / 100
            tmplday["AMO"] = struct.unpack("f", fp.read(4))[0]
            tmplday["VOL"] = struct.unpack("i", fp.read(4))[0]
            self.ldayvalue.append(tmplday)
        fp.close()
            
    def limitup ( self, n ):
        nclose = self.ldayvalue[n]["Close"]
        nbclose = self.ldayvalue[n+1]["Close"] + 0.0001
        if nclose == round((nbclose/10 + nbclose), 2):
            return True

    def limitdown ( self, n ):
        nclose = self.ldayvalue[n]["Close"]
        nbclose = self.ldayvalue[n+1]["Close"] + 0.0001
        if nclose == round((nbclose - nbclose/10), 2):
            return True

    def ma ( self, madaycount ):        
        for tmpday in range(len(self.ldayvalue) - madaycount + 1):
            sum = 0
            for c in range(madaycount):
                sum += self.ldayvalue[tmpday+c]["Close"]
            sum /= madaycount
            self.ldayvalue[tmpday]["ma{}".format(madaycount)] = sum

    def volma ( self, madaycount ):        
        for tmpday in range(len(self.ldayvalue) - madaycount + 1):
            sum = 0
            for c in range(madaycount):
                sum += self.ldayvalue[tmpday+c]["VOL"]
            sum /= madaycount
            self.ldayvalue[tmpday]["volma{}".format(madaycount)] = sum
            
    def gaodian ( self, n, gaodiandaycount ):
        tmpgd = self.ldayvalue[n]["High"]
        for tmpday in range( gaodiandaycount ):
            try:
                tmpgd = max(tmpgd, self.ldayvalue[n+tmpday]["High"])
            except:
                continue
        return tmpgd

    def didian ( self, n, didiandaycount ):
        tmpdd = self.ldayvalue[n]["Low"]
        for tmpday in range( didiandaycount ):
            try:
                tmpdd = min(tmpdd, self.ldayvalue[n+tmpday]["Low"])
            except:
                continue
        return tmpdd

    def cci ( self, ccidaycount ):
        for tmpday in range(len(self.ldayvalue) - ccidaycount + 1):
            typ = []
            for c in range(ccidaycount):
                typ.append((self.ldayvalue[c+tmpday]["High"] + self.ldayvalue[c+tmpday]["Low"]
                           + self.ldayvalue[c+tmpday]["Close"]) / 3)
            matyp = sum(typ) / ccidaycount
            absdiff = 0
            for c in range(ccidaycount):
                absdiff += abs(typ[c]-matyp)
            maabsdiff = absdiff / ccidaycount
            self.ldayvalue[tmpday]["cci{}".format(ccidaycount)] = (( typ[0] - matyp ) / ( maabsdiff * 0.015 ))
    def macd( self, eshort, elong, mid ):
        c = len(self.ldayvalue) - 1
        while (c > -1):
            if c != (len(self.ldayvalue) - 1):
                self.ldayvalue[c]["EMA{}".format(eshort)] = (self.ldayvalue[c+1]["EMA{}".format(eshort)])*(1-2/(eshort+1)) + self.ldayvalue[c]["Close"]*(2/(eshort+1))
                self.ldayvalue[c]["EMA{}".format(elong)] =  (self.ldayvalue[c+1]["EMA{}".format(elong)])*(1-2/(elong+1)) + self.ldayvalue[c]["Close"]*(2/(elong+1))
                self.ldayvalue[c]["DIF"] = self.ldayvalue[c]["EMA{}".format(eshort)] - self.ldayvalue[c]["EMA{}".format(elong)]
                self.ldayvalue[c]["DEA"] = self.ldayvalue[c+1]["DEA"]*(1-2/(mid+1)) + self.ldayvalue[c]["DIF"]*(2/(mid+1))
                self.ldayvalue[c]["MACD"] = 2 * (self.ldayvalue[c]["DIF"] - self.ldayvalue[c]["DEA"])
            else:
                self.ldayvalue[c]["EMA{}".format(eshort)] = self.ldayvalue[c]["Close"]
                self.ldayvalue[c]["EMA{}".format(elong)] = self.ldayvalue[c]["Close"]
                self.ldayvalue[c]["DIF"] = 0
                self.ldayvalue[c]["DEA"] = 0
                self.ldayvalue[c]["MACD"] = 0
            #print(self.code,self.ldayvalue[c]["DIF"],self.ldayvalue[c]["DEA"])
            c -= 1

    def kdj ( self, kdjdaycount, M1, M2 ):
        c = len(self.ldayvalue) - 1
        while (c > -1):
            gd = self.gaodian(c, kdjdaycount)
            dd = self.didian(c, kdjdaycount)
            self.ldayvalue[c]["RSV{}".format(kdjdaycount)] =(self.ldayvalue[c]["Close"]-dd)/(gd-dd)*100
            if c != (len(self.ldayvalue) - 1):
                self.ldayvalue[c]["K{}".format(kdjdaycount)] = ((self.ldayvalue[c+1]["K{}".format(kdjdaycount)])*2/3 + ((self.ldayvalue[c]["Close"]-dd)/(gd-dd)*100)/3)
                self.ldayvalue[c]["D{}".format(M1)] = ((self.ldayvalue[c+1]["D{}".format(M1)])*2/3 + self.ldayvalue[c]["K{}".format(kdjdaycount)]/3)
                self.ldayvalue[c]["J{}".format(M2)] = self.ldayvalue[c]["K{}".format(kdjdaycount)]*3 - self.ldayvalue[c]["D{}".format(M1)]*2
            else:
                self.ldayvalue[c]["K{}".format(kdjdaycount)] =(self.ldayvalue[c]["Close"]-dd)/(gd-dd)*100
                self.ldayvalue[c]["D{}".format(M1)] =(self.ldayvalue[c]["Close"]-dd)/(gd-dd)*100
                self.ldayvalue[c]["J{}".format(M2)] =(self.ldayvalue[c]["Close"]-dd)/(gd-dd)*100
#            print(self.ldayvalue[c]["K{}".format(kdjdaycount)],self.ldayvalue[c]["D{}".format(M1)],self.ldayvalue[c]["J{}".format(M2)])
            c -= 1

    def syxdyst ( self, n ):         #上影线大于实体
        if self.ldayvalue[n]["Close"] > self.ldayvalue[n]["Open"]:
            if (self.ldayvalue[n]["High"] - 2 * self.ldayvalue[n]["Close"] + self.ldayvalue[n]["Open"]) > 0:
                return True
        else:
            if (self.ldayvalue[n]["High"] - 2 * self.ldayvalue[n]["Open"] + self.ldayvalue[n]["Close"]) > 0:
                return True

    def lsvolzd( self ):       #历史成交量最大
        closex = 0
        volx = 0
        for x in range(len(self.ldayvalue)):
            if self.ldayvalue[x]["VOL"] > volx:
                volx = self.ldayvalue[x]["VOL"]
                closex = self.ldayvalue[x]["Close"]
        return closex
