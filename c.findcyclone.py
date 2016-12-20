from numpy import *
from detect_fsub import *
from datetime import datetime, timedelta
import util
import config_func
import IO_Master
import Cyclone
import calendar
import os, sys, shutil
#--------------------------------------------------
#prj     = "JRA55"
#model   = prj
#run     = ""
#res     = "bn"
#noleap  = False

prj     = "HAPPI"
model   = "MIROC5"
run     = "C20-ALL-001"
res     = "128x256"
noleap  = True

iDTime = datetime(2006,1,1,6)
eDTime = datetime(2006,1,31,18)
dDTime = timedelta(days=1)

ret_lDTime = {False: util.ret_lDTime
             ,True : util.ret_lDTime_noleap
             }[noleap]

lDTime   = ret_lDTime(iDTime, eDTime, dDTime)

tstp        = "6hr"

cfg    = config_func.config_func(prj, model, run)
iom    = IO_Master.IO_Master(prj, model, run, res)
cy     = Cyclone.Cyclone(cfg)

a1lat  = iom.Lat
a1lon  = iom.Lon
ny     = iom.ny
nx     = iom.nx
miss   = -9999.0
#####################################################
def var_psl(model):
  # variable name for mean sea level pressure
  if model in ["JRA25","JRA55"]:
    return "PRMSL"

def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#################################################
def mk_dir_tail(var, tstp, model, expr, ens):
  odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
       +ens
  return odir_tail
#####################################################
def mk_namehead(var, tstp, model, expr, ens):
  namehead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
       +ens
  return namehead
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#****************************************************
##**************************************************
## Mean Sea Level Pressure
##------------------------
#pslmeanname = pslmeandir_root + "/anl_surf125.PRMSL.0000000000.sa.one"
#a2pslmean = fromfile(pslmeanname, float32).reshape(ny, nx)
##------------------------
for DTime in lDTime:
  year = DTime.year
  mon  = DTime.month
  day  = DTime.day
  hour = DTime.hour
  pgraddir = cy.path_a2dat("pgrad",datetime(year,mon,1)).srcDir
  mk_dir(pgraddir)
  #***************************************
  #* names
  #---------------------------------------
  pgradname = cy.path_a2dat("pgrad",DTime).srcPath
  
  #***************************************
  a2psl   = iom.Load_6hrSfc("slp", DTime)
  findcyclone_out = detect_fsub.findcyclone_bn(a2psl.T, a1lat, a1lon, -9999.0, miss)
  a2pgrad = findcyclone_out.T
  a2pgrad.tofile(pgradname)

  print pgradname

