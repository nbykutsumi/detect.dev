from numpy import *
from datetime import datetime, timedelta
from front_fsub import *
from detect_fsub import *
import os
import socket
import ConstFront
import Reanalysis
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout


class Front(object):
  def __init__(self, model="JRA55", res="bn", miss=-9999.):
    #----------------
    hostname = socket.gethostname()
    if hostname == "well":
      self.rootDir  = "/media/disk2"
    if hostname in ["mizu","naam"]:
      self.rootDir  = "/tank/utsumi"
    #----------------


    C  = ConstFront.const(model=model, res=res)
    ra = Reanalysis.Reanalysis(model=model, res=res)

    self.res     = res
    if (model=="JRA25")&(res=="sa.one"):
      #self.baseDir = "/media/disk2/out/%s/%s.anl_p"%(model, res)
      self.baseDir = "%s/out/%s/%s.anl_p"%(self.rootDir, model, res)
    else:
      #self.baseDir = "/media/disk2/out/%s/%s"%(model, res)
      self.baseDir = "%s/out/%s/%s"%(self.rootDir, model, res)

    self.model   = model
    self.res     = res
    self.Lat     = read_txtlist( os.path.join(self.baseDir, "lat.txt"))
    self.Lon     = read_txtlist( os.path.join(self.baseDir, "lon.txt"))
    self.ny      = len(self.Lat)
    self.nx      = len(self.Lon)
    self.miss    = miss
    self.thgrids = C.thgrids
    self.Mt1     = C.thfmask(model,res)[0]
    self.Mt2     = C.thfmask(model,res)[1]
    self.Mq1     = C.thfmask(model,res)[2]
    self.Mq2     = C.thfmask(model,res)[3]
    self.thorog  = C.thorog
    self.thgradorog = C.thgradorog
    self.trace_coef = C.trace_coef
    #-- orog ------
    ny,nx      = self.ny, self.nx
    thorog     = self.thorog
    thgradorog = self.thgradorog

    srcDir     = ra.load_const("topo").srcDir
    self.maxorogname= os.path.join(srcDir, "maxtopo.0300km.%s"%(res))
    self.a2maxorog  = fromfile(self.maxorogname, float32).reshape(ny,nx)

    a2orogmask      = zeros([self.ny, self.nx], float32)*self.miss
    a2orogmask      = ma.masked_where(self.a2maxorog > thorog, a2orogmask)
    self.a2orogmask = a2orogmask
    #--------------


  def path_potloc(self, DTime, tq="t"):
    Year,Mon,Day,Hour = DTime.year, DTime.month, DTime.day, DTime.hour
    self.srcDir    = os.path.join( self.baseDir,"6hr", "front.%s"%(tq),"%04d"%Year,"%02d"%Mon)

    #-- test ---
    if (self.model=="JRA25")&(self.res=="sa.one"):
      self.srcDir    = os.path.join( self.baseDir,"6hr", "front.%s"%(tq),"%04d%02d"%(Year,Mon))

    #-----------

    self.srcPath1  = os.path.join( self.srcDir, "front.%s.M1.%04d.%02d.%02d.%02d.%s"%(tq,Year,Mon,Day,Hour,self.res))
    self.srcPath2  = os.path.join( self.srcDir, "front.%s.M2.%04d.%02d.%02d.%02d.%s"%(tq,Year,Mon,Day,Hour,self.res))

    return self


  def load_tfront(self, DTime, M1=False, M2=False):
    if type(M1)==bool:
      M1,M2 = self.Mt1, self.Mt2

    ny,nx     = self.ny, self.nx
    miss      = self.miss
    trace_coef= self.trace_coef

    Path      = self.path_potloc(DTime, "t")
    srcDir    = Path.srcDir
    srcPath1  = Path.srcPath1
    srcPath2  = Path.srcPath2

    a2potloc1 = fromfile(srcPath1, float32).reshape(ny,nx)
    a2potloc2 = fromfile(srcPath2, float32).reshape(ny,nx)
    a2loc     = ma.masked_less(a2potloc1, M1)
    a2loc     = ma.masked_where(a2potloc2 < M2, a2loc).filled(miss)

    a2loc     = ma.masked_where(self.a2orogmask.mask, a2loc).filled(miss)
    #- fill --
    a2trace   = ma.masked_less(a2potloc1, M1* trace_coef)
    a2trace   = ma.masked_where(a2potloc2 < M2* trace_coef, a2trace).filled(miss)
    a2loc     = front_fsub.fill_front_gap_trace(a2loc.T, a2trace.T, miss).T
    #---------
    a2loc     = front_fsub.del_front_lesseq_ngrids_wgt(a2loc.T, self.Lat,  miss, self.thgrids).T
    return a2loc

  def load_qfront(self, DTime, M1=False, M2=False, Mt1=False, Mt2=False):
    if type(M1)==bool:
      M1,M2 = self.Mq1, self.Mq2

    ny,nx     = self.ny, self.nx
    miss      = self.miss
    trace_coef= self.trace_coef

    Path      = self.path_potloc(DTime, "q")
    srcDir    = Path.srcDir
    srcPath1  = Path.srcPath1
    srcPath2  = Path.srcPath2

    a2potloc1 = fromfile(srcPath1, float32).reshape(ny,nx)
    a2potloc2 = fromfile(srcPath2, float32).reshape(ny,nx)

    a2loc     = ma.masked_less(a2potloc1, M1)
    a2loc     = ma.masked_where(a2potloc2 < M2, a2loc).filled(miss)

    a2loc_t   = self.load_tfront(DTime, Mt1, Mt2)
    a2loc_t   = detect_fsub.mk_territory_ngrids( a2loc_t.T, 2, miss).T
    a2loc     = ma.masked_where( a2loc_t !=miss, a2loc).filled(miss)

    a2loc     = ma.masked_where(self.a2orogmask.mask, a2loc).filled(miss)
    #- fill --
    a2trace   = ma.masked_less(a2potloc1, M1* trace_coef)
    a2trace   = ma.masked_where(a2potloc2 < M2* trace_coef, a2trace).filled(miss)
    a2loc     = front_fsub.fill_front_gap_trace(a2loc.T, a2trace.T, miss).T
    #---------
    a2loc     = front_fsub.del_front_lesseq_ngrids_wgt(a2loc.T, self.Lat, miss, self.thgrids).T

    return a2loc

  def mkMask_tfront(self, DTime, radkm=500, M1=False, M2=False, miss=False):

    if type(miss) == bool: miss = self.miss

    return detect_fsub.mk_territory(\
              self.load_tfront(DTime, M1=M1, M2=M2).T, self.Lon, self.Lat, radkm*1000., imiss=self.miss, omiss=miss\
                                   ).T
 
  def mkMask_qfront(self, DTime, radkm=500, M1=False, M2=False, Mt1=False, Mt2=False, miss=False):

    if type(miss) == bool: miss = self.miss

    return detect_fsub.mk_territory(\
              self.load_qfront(DTime, M1=M1, M2=M2, Mt1=Mt1, Mt2=Mt2).T, self.Lon, self.Lat, radkm*1000., imiss=self.miss, omiss=miss\
                                   ).T
 
    

