from numpy import *
#import JRA55
#import JRA25
import Reanalysis
import Front
import calendar
import detect_func
import sys, os
import datetime
import ConstFront
#from dtanl_fsub import *
from front_fsub import *
#-----------------------
#lyear  = range(2010,2014+1)
#lyear  = range(1980,2012+1)
lyear  = range(1990,2009)
#lyear  = [2004]
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#iday   = 1
iday   = 1  # test
lhour  = [0,6,12,18]
ltq    = ["t","q"]
#ltq    = ["t"]
model  = "JRA55"
res    = "bn"
#model  = "JRA25"
#res    = "bn"
#res    = "sa.one"

ra     = Reanalysis.Reanalysis(model=model, res=res)
if   model=="JRA55":
  dvar   = {"t":"tmp", "q":"spfh"}

elif (model=="JRA25"):
  dvar   = {"t":"TMP", "q":"SPFH"}


front  = Front.Front(model,res)
ConstF = ConstFront.Const(model=model, res=res)
#------------------------
#local region ------
plev     = 850   #(hPa)
cbarflag = "True"
#-------------------

miss  = -9999.0

#thorog  = ctrack_para.ret_thorog()
#thgradorog=ctrack_para.ret_thgradorog()
thorog     = ConstF.thorog
thgradorog = ConstF.thgradorog

#************************
# FUNCTIONS
#************************
# lat & lon
#--------------
a1lat = ra.Lat
a1lon = ra.Lon
#*************************
# front locator :contour
#---------------
def mk_front_loc_contour(a2thermo, a1lon, a1lat, miss):
  a2fmask1 = front_fsub.mk_a2frontmask1(a2thermo.T, a1lon, a1lat, miss).T
  a2fmask2 = front_fsub.mk_a2frontmask2(a2thermo.T, a1lon, a1lat, miss).T
  a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]

  a2loc    = front_fsub.mk_a2meanaxisgrad3_h98_eq6(a2thermo.T, a1lon, a1lat, miss).T

  a2loc    = front_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss).T
  a2loc    = ma.masked_equal(a2loc, miss)  

  a2loc    = ma.masked_where(a2fmask1 < 0.0, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < 0.0, a2loc)
  a2loc1   = ma.masked_where(a2loc.mask, a2fmask1).filled(miss)
  a2loc2   = ma.masked_where(a2loc.mask, a2fmask2).filled(miss)

  return a2loc1, a2loc2

#******************************************************
##-- orog & grad orog ----

a2orog  = ra.load_const(var="topo").Data

#******************************************************
for year in lyear:
  for mon in lmon:
    eday  = calendar.monthrange(year,mon)[1]
    for tq in ltq:
      var = dvar[tq]
      #-----------
      for day in range(iday, eday+1):
        for hour in lhour:
          DTime   = datetime.datetime(year,mon,day,hour)
          ##******************************************************
          a2thermo  = ra.load_6hr(var, DTime, plev).Data
          a2loc1,a2loc2  = mk_front_loc_contour(a2thermo, a1lon, a1lat, miss)
          sodir, soname1, soname2   = front.path_potloc(DTime, tq)
          detect_func.mk_dir(sodir)
          #------
          a2loc1.tofile(soname1)
          a2loc2.tofile(soname2)
          print soname1
          print soname2
  
 
