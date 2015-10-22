from numpy import *
from detect_fsub import *
from datetime import datetime, timedelta
from collections import deque
import os
import itertools
import socket
import BestTrackTC
from ConstCyclone import Const
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout

def ret_baseDir(model="JRA55", res="bn"):
  hostname     = socket.gethostname()
  if hostname == "well":
    return "/media/disk2/out/%s/%s"%(model,res)
  elif hostname in ["mizu","naam"]:
    return "/tank/utsumi/out/%s/%s"%(model,res)

#---------------------------------------------------
def solve_time(stime):
  year = int( stime/10**6 )
  mon  = int( (stime - year*10**6)/10**4 )
  day  = int( (stime - year*10**6 - mon*10**4)/10**2)
  hour = int( (stime - year*10**6 - mon*10**4 - day*10**2) )
  return year, mon, day, hour
#---------------------------------------------------
def fortpos2pyxy(number, nx, miss_int):
  if (number == miss_int):
    iy_py = miss_int
    ix_py = miss_int
  else:
    iy_py = int((number-1.0)/nx)      # iy_py = 0,1,2,..
    ix_py = number - nx*iy_py-1   # ix_py = 0,1,2,..
  #----
  return ix_py, iy_py
#---------------------------------------------------
def expand8grids(lxy, ny, nx):
  # lxy = [(x1,y1), (x2,y2), ...]
  if len(lxy) == 0:
    lXY = array([])
  else:
    lXY = deque([])
    for x,y in lxy:
      lXY.extend(list(itertools.product([x-1,x,x+1],[y-1,y,y+1])))
  
    ax, ay = zip(*lXY)
    ax = ma.masked_equal(ax,-1).filled(nx-1)
    ax = ma.masked_equal(ax,nx).filled(0)
    ay = ma.masked_equal(ay,-1).filled(0)
    ay = ma.masked_equal(ay,ny).filled(ny-1)
  
    lXY = array(zip(ax,ay))
  return  lXY
  
#---------------------------------------------------
class Cyclone(Const):
  def __init__(self, model="JRA55", res="bn"):
    Const.__init__(self, model=model, res=res)
    self.baseDir = ret_baseDir(model=model, res=res)
    #------------
    self.Lat     = read_txtlist( os.path.join(self.baseDir, "lat.txt"))
    self.Lon     = read_txtlist( os.path.join(self.baseDir, "lon.txt"))
    self.ny      = len(self.Lat)
    self.nx      = len(self.Lon)
    self.dNumType= {"life"    :int32,
                    "dura"    :int32,
                    "ipos"    :int32,
                    "idate"   :int32,
                    "time"    :int32,
                    "nowpos"  :int32,
                    "lastpos" :int32,
                    "nextpos" :int32,
                    "pgrad"   :float32,
                    "pgmax"   :float32,
                    "pmean"   :float32,
                    #"iedist"  :float32,
                    "rvort"   :float32,
                    "dtlow"   :float32,
                    "dtmid"   :float32,
                    "dtup"    :float32,
                    "wmeanlow":float32,
                    "wmeanup" :float32,
                    "sst"     :float32,
                    "land"    :float32,
                    "initsst" :float32,
                    "initland":float32
                   }

  def path_a2dat(self, var, DTime):
    Year = DTime.year
    Mon  = DTime.month
    Day  = DTime.day
    Hour = DTime.hour
    self.tstep   = "6hr"
    self.srcDir  = os.path.join(self.baseDir, self.tstep, var, "%04d"%(Year), "%02d"%(Mon))
    self.srcPath = os.path.join(self.srcDir, "%s.%04d%02d%02d%02d.bn"%(var,Year,Mon,Day,Hour))
    return self

  def load_a2dat(self, var, DTime):
    srcPath = self.path_a2dat(var, DTime)
    a2dat = fromfile(self.srcPath, self.dNumType[var]).reshape(self.ny,self.nx)
    return a2dat

  def path_clist(self, var, Year, Mon):
    self.tstep   = "6hr"
    self.srcDir  = os.path.join(self.baseDir, self.tstep, "clist", "%04d"%(Year), "%02d"%(Mon))
    self.srcPath = os.path.join(self.srcDir, "%s.%04d.%02d.bn"%(var,Year,Mon))
    return self

  def load_clist(self, var, Year, Mon):
    srcPath = self.path_clist(var, Year, Mon)
    return fromfile(self.srcPath, self.dNumType[var])

  def dictC(self, Year, Mon, varname="pgrad", tctype="obj"):
   if tctype == "obj":
     return self.dictC_objTC(Year, Mon, varname=varname, tctype=tctype)
   if tctype == "bst":
     return self.dictC_bstTC(Year, Mon, varname=varname, tctype=tctype)



  def dictC_bstTC(self, Year, Mon, varname="pgrad", tctype="obj"):
    thpgrad   = self.thpgrad
    thdura    = self.thdura

    dictExC   = {}
    dictTC    = {}
    da1       = {}

    #--- TC dictionary ----
    bst       = BestTrackTC.BestTrack("IBTrACS")
    dictTC    = bst.ret_dpyxy(Year, self.Lon, self.Lat)

 
    #---- make ExC dictionary -----
    lvar      = ["dura","pgrad","nowpos","time"]
    for var in lvar:
       da1[var]  = self.load_clist(var, Year, Mon)

    dtcloc   = {}
    nlist    = len(da1["dura"])

    for i in range(nlist):
      dura        = da1["dura"    ][i]
      pgrad       = da1["pgrad"   ][i]
      nowpos      = da1["nowpos"  ][i]
      time        = da1["time"    ][i]
      oVar        = da1[varname][i]
      #---- dura -------
      if dura < thdura:
        #print "dura",dura,"<",thdura
        continue
      #---- thpgrad ----
      if pgrad < thpgrad:
        #print "pgrad",pgrad,"<",thpgrad
        continue
  
      #---- time -------
      Year,Mon,Day,Hour = solve_time(time)
      DTime             = datetime(Year,Mon,Day,Hour)
  
      #---- nowpos  ----
      x,y               = fortpos2pyxy(nowpos, self.nx, -9999)


      #-- check TC ----
      lxyTC  = expand8grids(dictTC[DTime], self.ny, self.nx)
      if [x,y] in lxyTC:
        continue 
 
      #-- List  -------
      oList  = [x,y,oVar] 


      try:
        dictExC[DTime].append(oList)
      except KeyError:
        dictExC[DTime] = [oList]
    #--------------------------------------------
    self.dictTC  = dictTC
    self.dictExC = dictExC
    return self


  def dictC_objTC(self, Year, Mon, varname="pgrad", tctype="obj"):
    thrvort   = self.thrvort
    thpgrad   = self.thpgrad
    thwcore   = self.thwcore
    thdura    = self.thdura
    thinitsst = self.thsst 

    dictExC   = {}
    dictTC    = {}
    da1       = {}

    #lvar      = ["dura","pgrad","nowpos","nextpos","time","iedist","rvort","dtlow","dtmid","dtup","initsst","initland"]
    lvar      = ["dura","pgrad","nowpos","time","rvort","dtlow","dtmid","dtup","initsst","initland"]
    for var in lvar:
       da1[var]  = self.load_clist(var, Year, Mon)
  
    #---- make dictionary -----
    dtcloc   = {}
    nlist    = len(da1["dura"])
    for i in range(nlist):
      dura        = da1["dura"    ][i]
      pgrad       = da1["pgrad"   ][i]
      nowpos      = da1["nowpos"  ][i]
      time        = da1["time"    ][i]
      #iedist      = da1["iedist"  ][i]
      rvort       = abs(da1["rvort"   ][i])
      dtlow       = da1["dtlow"   ][i]
      dtmid       = da1["dtmid"   ][i]
      dtup        = da1["dtup"    ][i]
      initsst     = da1["initsst" ][i]
      initland    = da1["initland"][i]
      #nextpos     = da1["nextpos" ][i]

      oVar        = da1[varname][i]
      #---- dura -------
      if dura < thdura:
        #print "dura",dura,"<",thdura
        continue
      #---- thpgrad ----
      if pgrad < thpgrad:
        #print "pgrad",pgrad,"<",thpgrad
        continue
  
      #---- time -------
      Year,Mon,Day,Hour = solve_time(time)
      DTime             = datetime(Year,Mon,Day,Hour)
  
      #---- nowpos  ----
      x,y               = fortpos2pyxy(nowpos, self.nx, -9999)
  
      #-- List  -------
      oList  = [x,y,oVar] 

      #---- thrvort ----
      if rvort < thrvort:
        #print "rvort",rvort,"<",thrvort
        try:
          dictExC[DTime].append(oList)
        except KeyError:
          dictExC[DTime] = [oList]
  
        continue
  
      #---- thwcore ----
      if dtup + dtmid + dtlow < thwcore:
        #print "thwcore",dtup+dtmid+dtlow,"<",thwcore
        try:
          dictExC[DTime].append(oList)
        except KeyError:
          dictExC[DTime] = [oList]
  
        continue
  
      #---- initsst ----
      if initsst < thinitsst:
        #print "initsst",initsst,"<",thinitsst
        try:
          dictExC[DTime].append(oList)
        except KeyError:
          dictExC[DTime] = [oList]
  
        continue
  
      #---- initland ----
      if initland > 0.0:
        #print "initland",initland,">",0.0
        try:
          dictExC[DTime].append(oList)
        except KeyError:
          dictExC[DTime] = [oList]
  
        continue
  
      #---- TC ----
      try:
        dictTC[DTime].append(oList)
      except KeyError:
        dictTC[DTime] = [oList]

    #--------------------------------------------
    self.dictTC  = dictTC
    self.dictExC = dictExC
    return self


class Cyclone_2D(Cyclone):
  def __init__(self, Year, Mon, model="JRA55", tctype="obj",miss=-9999.):


    Cyclone.__init__(self)
    self.instDict  = self.dictC(Year, Mon, varname="pgrad",tctype=tctype)
    self.a2miss    = ones([self.ny, self.nx], float32)*miss
    self.miss      = miss
    self.tctype    = tctype



  def load_a2tc(self, DTime):
    aList     = zip(*array(self.instDict.dictTC[DTime]))
    a2dat     = self.a2miss.copy()
    a2dat[ aList[1], aList[0]] = aList[-1]
    return a2dat

  def load_a2exc(self, DTime):
    aList     = zip(*array(self.instDict.dictExC[DTime]))
    a2dat     = self.a2miss.copy()
    a2dat[ aList[1], aList[0]] = aList[-1]
    return a2dat

  def mkMask_exc(self, DTime, radkm=1000, miss=False):
    if type(miss) == bool: miss=self.miss

    a2loc     = self.load_a2exc(DTime)
    return detect_fsub.mk_territory(a2loc.T, self.Lon, self.Lat, radkm*1000., imiss=self.miss, omiss=miss).T

  def mkMask_tc(self, DTime, radkm=1000, miss=False):
    if type(miss) == bool: miss=self.miss
    a2loc     = self.load_a2tc(DTime)
    return detect_fsub.mk_territory(a2loc.T, self.Lon, self.Lat, radkm*1000., imiss=self.miss, omiss=miss).T


