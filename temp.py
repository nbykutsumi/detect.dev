from numpy import *
from datetime import datetime, timedelta
import Cyclone
import JRA55
Year = 2010
Mon  = 1
Day  = 1
Hour = 0
DTime = datetime(Year,Mon,Day,Hour)
model = "JRA55"
res   = "bn"
jra   = JRA55.Jra55(res="bn")
Lat = jra.Lat
Lon = jra.Lon

X,Y  = meshgrid(Lon,Lat)
d={}
for i in range(20):
  DTime = DTime + timedelta(hours=6)
  C=Cyclone.Cyclone_2D(Year,Mon,model=model,res=res,tctype="bst",miss=-9999.)
  #a = C.mkMask_tc(DTime, radkm=1000)
  a = C.mk_a2tc(DTime)
  x = ma.masked_where(a==-9999., X)
  y = ma.masked_where(a==-9999., Y)
  d[i] = a
  print DTime, a.max(), x.compressed(), y.compressed()


