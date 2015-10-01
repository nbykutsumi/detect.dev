import sys, datetime
import Cyclone
from numpy import *
from collections import deque

iyear  = 2004
eyear  = 2004
lyear  = range(iyear,eyear+1)
#lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
lmon   = [2,3,4,5,6]
model  = "JRA55"
res    = "bn"
#--- year and month when the first data available --
iyear_data = 2004
imon_data  = 2
#-------------
cyclone= Cyclone.Cyclone(model, res)
#**********************************************
def ret_a1initState(var, year,mon,dinitState_pre):
  #----------
  dinitState              = {}
  dinitState[-9999,-9999] = -9999.0
  #----------
  a1idate     = cyclone.load_clist("idate",year,mon) 
  a1ipos      = cyclone.load_clist("ipos" ,year,mon) 
  a1time      = cyclone.load_clist("time" ,year,mon) 
  a1state     = cyclone.load_clist(var    ,year,mon) 
  a1land      = cyclone.load_clist("land" ,year,mon) 

  #------------------------
  n  = len(a1idate)
  ldat    = deque([])
  for i in range(n):
    idate = a1idate[i]
    ipos  = a1ipos [i]
    time  = a1time [i]
    state = a1state[i]
    #print idate, ipos, time
    #--- check initial time --
    if time == idate:
      dinitState[idate, ipos] = state

    #-----------
    try:
      ldat.append( dinitState[idate, ipos] )
    except KeyError:
      try:
        ldat.append( dinitState_pre[idate, ipos])
      except:
        ldat.append( -9999.0)
#        sys.exit() 
  #---------------------------
  a1initState = array(ldat, float32)
  return dinitState, a1initState
#**********************************************

#--- init ----
imon       = lmon[0]
date_first = datetime.date(iyear,imon, 1)
date_pre   = date_first + datetime.timedelta(days = -2)
year_pre   = date_pre.year
mon_pre    = date_pre.month
if (iyear == iyear_data)&(imon ==imon_data):
  dinitsst   = {} 
  dinitland  = {} 
else:
  dinitsst , a1temp = ret_a1initstate("sst" , year_pre, mon_pre, {} )
  dinitland, a1temp = ret_a1initstate("land", year_pre, mon_pre, {} )
#-------------
for year, mon in [[year,mon] for year in lyear for mon in lmon]:
  dinitsst_pre          = dinitsst
  dinitsst, a1initsst   = ret_a1initState( "sst", year, mon, dinitsst_pre )

  dinitland_pre         = dinitland
  dinitland, a1initland = ret_a1initState( "land",year, mon, dinitland_pre )
 
 
  #---- oname ----------------
  name_sst  = cyclone.path_clist("initsst" ,year,mon).srcPath
  name_land = cyclone.path_clist("initland",year,mon).srcPath
  a1initsst.tofile(name_sst)
  a1initland.tofile(name_land)
  print name_sst

  
