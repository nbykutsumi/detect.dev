from numpy import *
from datetime import datetime, timedelta
import os

#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout


class Cyclone(object):
  def __init__(self, model="JRA55", res="bn"):
    self.baseDir = "/media/disk2/out/%s/%s"%(model,res)
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
                    "iedist"  :float32,
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
    a2dat = fromfile(self.srcPath, self.dNumType[var])
    return a2dat
 
   
