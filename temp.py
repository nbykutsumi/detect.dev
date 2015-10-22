import Tag
import Cyclone
import Front
import JRA55
from datetime import datetime
import BestTrackTC
Year = 2004
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

dictMask = T.mkMask_wgt(["c","tc","fbc","nbc"], DTime)

print dictMask 
