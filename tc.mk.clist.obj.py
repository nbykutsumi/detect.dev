from numpy import *
from collections import deque
from datetime import datetime, timedelta
from detect_fsub import *
import detect_func
import calendar
import Reanalysis
import Cyclone

lYear = [2014]
lMon  = range(1,12+1)
model = "JRA55"
res   = "bn"
lHour = [0,6,12,18]
miss  = -9999.
lvar  = ["rvort", "dtlow", "dtmid", "dtup", "wmeanlow", "wmeanup", "sst","land"]


ra   = Reanalysis.Reanalysis(model=model,res=res)

cyclone = Cyclone.Cyclone(model=model,res=res)

a1lat = cyclone.Lat
a1lon = cyclone.Lon

def ret_dvarname(model):
  if   model in ["JRA25"]:
    return {"ua":"UGRD", "va":"VGRD", "ta":"TMP","sst":"WTMPsfc","land":"land"}
  elif model in ["JRA55"]:
    return {"ua":"ugrd", "va":"vgrd", "ta":"tmp","sst":"BRTMP","land":"land"}

def save_clist(var, a1dat, Year, Mon):
  clistPath = cyclone.path_clist(var, Year, Mon).srcPath
  clistDir  = cyclone.path_clist(var, Year, Mon).srcDir
  detect_func.mk_dir(clistDir)
  dNumType  = cyclone.dNumType
  array(a1dat, dtype=dNumType[var]).tofile(clistPath)  
  print clistPath

def ret_a2pgrad(DTime):
  return cyclone.load_a2dat("pgrad", DTime) 

#----------------------------
dvarname = ret_dvarname(model)
var_ta   = dvarname["ta"]
var_va   = dvarname["va"]
var_ua   = dvarname["ua"]
var_sst  = dvarname["sst"]
var_land = dvarname["land"]
#----------------------------
for Year in lYear:
  for Mon in lMon:
    #*** init ***********
    da1 = {}
    for var in lvar:
      da1[var]  = deque([])
    #********************
    # SST
    #-------------------- 
    a2sst = ra.load_mon(var_sst, Year, Mon).Data

    #********************
    # Land
    #-------------------- 
    a2land= ra.load_const(var_land).Data
    #-------------------- 
    iDay = 1
    eDay = calendar.monthrange(Year,Mon)[1]
    for Day,Hour in [[Day,Hour] for Day in range(iDay,eDay+1) for Hour in lHour]:
      DTime = datetime(Year,Mon,Day,Hour)

      a2pgrad = cyclone.load_a2dat("pgrad",DTime)
      a2tlow  = ra.load_6hr(var_ta,DTime,850).Data
      a2tmid  = ra.load_6hr(var_ta,DTime,500).Data
      a2tup   = ra.load_6hr(var_ta,DTime,250).Data
      a2ulow  = ra.load_6hr(var_ua,DTime,850).Data
      a2uup   = ra.load_6hr(var_ua,DTime,250).Data
      a2vlow  = ra.load_6hr(var_va,DTime,850).Data
      a2vup   = ra.load_6hr(var_va,DTime,250).Data
      
      tout = detect_fsub.calc_tcvar\
            (  a2pgrad.T, a2tlow.T, a2tmid.T, a2tup.T\
             , a2ulow.T, a2uup.T, a2vlow.T, a2vup.T\
             , a1lon, a1lat\
             , miss\
            )

      a2rvort    = tout[0].T 
      a2dtlow    = tout[1].T 
      a2dtmid    = tout[2].T 
      a2dtup     = tout[3].T 
      a2wmeanlow = tout[4].T 
      a2wmeanup  = tout[5].T 

      #---- shrink ---------------------
      a1rvort_tmp     = ma.masked_where( a2pgrad==miss, a2rvort    ).compressed()
      a1dtlow_tmp     = ma.masked_where( a2pgrad==miss, a2dtlow    ).compressed()
      a1dtmid_tmp     = ma.masked_where( a2pgrad==miss, a2dtmid    ).compressed()
      a1dtup_tmp      = ma.masked_where( a2pgrad==miss, a2dtup     ).compressed()
      a1wmeanlow_tmp  = ma.masked_where( a2pgrad==miss, a2wmeanlow ).compressed()
      a1wmeanup_tmp   = ma.masked_where( a2pgrad==miss, a2wmeanup  ).compressed()
      a1sst_tmp       = ma.masked_where( a2pgrad==miss, a2sst      ).compressed()
      a1land_tmp      = ma.masked_where( a2pgrad==miss, a2land     ).compressed()

      da1["rvort"   ].extend( a1rvort_tmp   )
      da1["dtlow"   ].extend( a1dtlow_tmp   )
      da1["dtmid"   ].extend( a1dtmid_tmp   )
      da1["dtup"    ].extend( a1dtup_tmp    )
      da1["wmeanlow"].extend( a1wmeanlow_tmp)
      da1["wmeanup" ].extend( a1wmeanup_tmp )
      da1["sst"     ].extend( a1sst_tmp     )
      da1["land"    ].extend( a1land_tmp    )
    #- write clist --
    for var in lvar:
      save_clist(var, da1[var], Year, Mon) 
