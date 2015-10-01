from numpy import *
from detect_fsub import *
from datetime import datetime
from collections import deque
import os
import calendar
import JRA55
import Cyclone
import ctrack_func

model  = "JRA55"
res    = "bn"
iYear  = 2004
eYear  = 2004
lYear  = range(iYear,eYear+1)
lMon   = [1,3,5,7,9,11]
#lMon   = [1]
lHour  = [0,12]

#******************************
def save_csv(var, ldat):
  """
  var: rvort, dt, wmeanlow, wmeanup
  """
  ldat   = sort(ldat)
  lendat = len(ldat)

  dunit  = {"rvort":"s-1",
            "dt"   :"K",
            "wLow_Up":"m/s",
            "pgrad":"Pa/1000km"
           }

  sout = "frac/%s(%s),%s\n"%(model,var,dunit[var])
  for i,dat in enumerate(ldat):
    frac = (i+1)/float(lendat)
    sout = sout + "%f,%f\n"%(frac,dat)

  #
  odir   = "/media/disk2/out/obj.valid/c.%s"%(var)
  ctrack_func.mk_dir(odir)
  oname  = odir + "/%s.%s.%04d-%04d.%s.csv"%(var,model,iYear,eYear,"ASAS")

  f = open(oname,"w");  f.write(sout);  f.close()
  print oname
#******************************

def nearest_idx(aSrc,val):
    ''' return nearest index. by HJKIM'''
    if hasattr(val,'__iter__'): return [abs(aSrc-v).argmin() for v in val]
    else: return abs(aSrc-val).argmin()
#******************************
def mk_saone2bnxy(a1lon_bn, a1lat_bn):
  a1lon_saone = arange(0.5,359.5+0.01,1.0)
  a1lat_saone = arange(-89.5, 89.5+0.01, 1.0)

  a1corres_x  = nearest_idx(a1lon_bn, a1lon_saone)
  a1corres_y  = nearest_idx(a1lat_bn, a1lat_saone)
  a2corres_x, a2corres_y = meshgrid(a1corres_x, a1corres_y)
  return a2corres_x, a2corres_y

def load_chart(Year,Mon,Day,Hour):
  srcDir  = "/media/disk2/out/chart/ASAS/exc/%04d%02d"%(Year,Mon)
  #srcPath = os.path.join(srcDir, "exc.ASAS.2004.01.04.12.sa.one")
  srcPath = os.path.join(srcDir, "exc.ASAS.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Day,Hour))
  a2dat   = fromfile(srcPath, float32).reshape(180,360)
  return a2dat
#******************************
#-- Reanalysis --
ra    = JRA55.Jra55(res)
a1lat = ra.Lat
a1lon = ra.Lon
ny    = ra.ny
nx    = ra.nx
miss  = -9999.

#-- Cyclone -----
cyclone = Cyclone.Cyclone(model,res)

#----------------
a2miss  = ones([ny,nx],float32)*miss
a2corres_x, a2corres_y = mk_saone2bnxy(a1lon, a1lat)
print a2corres_x

#-- initialize --
lpgrad  = deque([])
#----------------

for Year in lYear:
  for Mon in lMon:
    print Year,Mon
    eDay  = calendar.monthrange(Year,Mon)[1]
    lDay  = range(1,eDay+1)
    for Day, Hour in [[Day,Hour] for Day in lDay for Hour in lHour]:
      #-- chart territory ----
      a2chart_one = load_chart(Year,Mon,Day,Hour)
      a1x         = ma.masked_where(a2chart_one==0.0, a2corres_x).compressed()
      a1y         = ma.masked_where(a2chart_one==0.0, a2corres_y).compressed()
      a2chart_bn  = a2miss.copy() 
      a2chart_bn[a1y,a1x] = 1.0
      a2chart_bn  = detect_fsub.mk_territory(a2chart_bn.T, a1lon, a1lat, 200*1000.,miss).T

      #-- load cyclone from reanalysis --
      DTime   = datetime(Year,Mon,Day,Hour)
      a2pgrad = cyclone.load_a2dat("pgrad",DTime)
      a2pgrad = ma.masked_where(a2chart_bn==miss, a2pgrad).filled(miss)
      a2pgrad = ma.masked_equal(a2pgrad, miss)
      #-- stack ---
      lpgrad.extend( a2pgrad.compressed() )

#-- save ----
save_csv("pgrad",lpgrad)


