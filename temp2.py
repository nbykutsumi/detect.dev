from numpy import *
import Tag
import regrid.Regrid as Regrid
#import cf
from datetime import datetime
Year = 2010
Mon  = 3
Day  = 1
Hour = 0
DTime = datetime(Year,Mon,Day,Hour)
model = "JRA55"
res   = "bn"

T     = Tag.Tag(model,res)
instMon = T.init_cyclone(Year,Mon)

a2t = T.mkMask("front.t",DTime, miss=0.0)
a2q = T.mkMask("front.q",DTime, miss=0.0)
a2c = T.mkMask("c",DTime)
a2cf = T.mkMask("cf",DTime)

LatIn = T.Front.Lat
LonIn = T.Front.Lon
LatOut = arange(-89.75,89.75+0.01, 0.5)
LonOut = arange(0.25, 359.75+0.01, 0.5)

a2T = Regrid.biIntp(LatIn, LonIn, a2t, LatOut, LonOut)
#a2T = cf.regrids(LatIn, LonIn, a2t, LatOut, LonOut)
print shape(a2t)
#print shape(LatIn)
#print shape(LonIn)
print shape(a2T)
#print a2t
#print a2T

