from numpy import *
from datetime import datetime
import os, sys
#**********************************************
class Jra25saone():
  def __init__(self):
    self.baseDir  = "/media/disk2/data/JRA25"
    self.Lat      = array(arange(-89.5, 89.5+0.01, 1.0), float32)
    self.Lon      = array(arange(0.5, 359.5+0.01, 1.0), float32)
    self.ny       = 180
    self.nx       = 360


  def load_6hr(self, var, DTime, lev=False):
    Year = DTime.year
    Mon  = DTime.month
    Day  = DTime.day
    Hour = DTime.hour

    if  var in ["SPFH","TMP","UGRD","VGRD"]:
      self.srcDir  = os.path.join(self.baseDir, "sa.one.anl_p","6hr", var, "%04d%02d"%(Year,Mon))
      self.srcPath = os.path.join(self.srcDir, "anl_p.%s.%04dhPa.%04d%02d%02d%02d.sa.one"%(var,lev,Year,Mon,Day,Hour))

    elif var in ["PRMSL"]:
      self.srcDir  = os.path.join(self.baseDir, "sa.one.anl_p","6hr", var, "%04d%02d"%(Year,Mon))
      self.srcPath = os.path.join(self.srcDir, "anl_p.%s.%04d%02d%02d%02d.sa.one"%(var,Year,Mon,Day,Hour))
    else:
      print "JRA25.py: check variable",var
      sys.exit()

    self.Data    = fromfile(self.srcPath, float32).reshape(self.ny, self.nx)
    return self


  def load_const(self, var, miss=False):
    """
    topo
    """
    if var == "topo":
      self.srcDir  = "/media/disk2/data/JRA25/sa.one.125/const/%s"%(var)
      self.srcPath = os.path.join(self.srcDir, "%s.sa.one"%(var))

    self.Data    = fromfile(self.srcPath, float32).reshape(self.ny, self.nx)
    return self

class Jra25():
  def __init__(self, res="bn"):
    self.baseDir  = "/media/disk2/data/JRA25"
    self.Lat      = array(arange(-90, 90+0.001, 1.25),  float32)
    self.Lon      = array(arange(0, 358.75+0.001, 1.25),float32)
    self.ny       = 145
    self.nx       = 288
    self.res      = res

  def load_6hr(self, var, DTime, lev=False):
    res  = self.res
    Year = DTime.year
    Mon  = DTime.month
    Day  = DTime.day
    Hour = DTime.hour

    if  var in ["SPFH","TMP","UGRD","VGRD"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_p"%(res),"6hr", var, "%04d%02d"%(Year,Mon))
      self.srcPath = os.path.join(self.srcDir, "anl_p.%s.%04dhPa.%04d%02d%02d%02d.%s"%(var,lev,Year,Mon,Day,Hour,res))

    elif var in ["PRMSL"]:
      self.srcDir  = os.path.join(self.baseDir, "%s.anl_p"%(res),"6hr", var, "%04d%02d"%(Year,Mon))
      self.srcPath = os.path.join(self.srcDir, "anl_p.%s.%04d%02d%02d%02d.%s"%(var,Year,Mon,Day,Hour,res))
    else:
      print "JRA25.py: check variable",var
      sys.exit()

    self.Data    = fromfile(self.srcPath, float32).reshape(self.ny, self.nx)
    return self


  def load_const(self, var, miss=False):
    """
    topo
    """
    res  = self.res
    if var == "topo":
      self.srcDir  = "/media/disk2/data/JRA25/%s.125/const/%s"%(res, var)
      self.srcPath = os.path.join(self.srcDir, "%s.%s"%(var, res))

    self.Data    = fromfile(self.srcPath, float32).reshape(self.ny, self.nx)
    return self


