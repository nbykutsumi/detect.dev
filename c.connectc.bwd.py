from numpy import *
from detect_fsub import *
import Reanalysis
import Cyclone
import ConstCyclone
import calendar
import datetime
import os, sys
##***************************
#--------------------------------------------------
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["anl_p125"]
lmodel   = ["JRA55"]
res     = "bn"
hinc    = 6
dDTime  = datetime.timedelta(hours=hinc)
#flgresume  = True
flgresume  = False
#------------------------
iYM   = [2014,2]
eYM   = [2014,2]

iyear, imon = iYM
eyear, emon = eYM
#****************
miss_dbl     = -9999.0
miss_int     = -9999
endh         = 18
thdp         = 0.0  #[Pa]
thdist_search = 500.0*1000.0   #[m]
#####################################################

#####################################################
# functions
#####################################################
def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]

#####################################################
def ret_var_ua(model):
  if model in ["JRA25"]:
    return "UGRD"
  elif model in ["JRA55"]:
    return "ugrd"

#####################################################
def ret_var_va(model):
  if model in ["JRA25"]:
    return "VGRD"
  elif model in ["JRA55"]:
    return "vgrd"
#####################################################
def ret_var_topo(model):
  if model in ["JRA25","JRA55"]:
    return "topo"
#####################################################
def pyxy2fortpos(ix, iy, nx):
  ix     = ix + 1  # ix = 1,2,.. nx
  iy     = iy + 1  # iy = 1,2,.. ny
  #number = iy* nx + ix +1
  number = (iy-1)* nx + ix
  return number
#####################################################
def fortpos2pyxy(number, nx, miss_int):
  if (number == miss_int):
    iy0 = miss_int
    ix0 = miss_int
  else:
    iy0 = int((number-1)/nx)  +1  # iy0 = 1, 2, ..
    ix0 = number - nx*(iy0-1)     # ix0 = 1, 2, ..

    iy0 = iy0 -1    # iy0 = 0, 1, .. ny-1
    ix0 = ix0 -1    # ix0 = 0, 1, .. nx-1
  #----
  return ix0, iy0
#####################################################
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
#####################################################
def date_slide(year,mon,day, daydelta):
  today       = datetime.date(year, mon, day)
  target      = today + datetime.timedelta(daydelta)
  targetyear  = target.year
  #***********
  #if ( calendar.isleap(targetyear) ):
  #  leapdate   = datetime.date(targetyear, 2, 29)
  #  #---------
  #  if (target <= leapdate) & (leapdate < today):
  #    target = target + datetime.timedelta(-1)
  #  elif (target >= leapdate ) & (leapdate > today):
  #    target = target + datetime.timedelta(1)
  #-----------
  return target
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#******************************************************
for model in lmodel:
  ra       = Reanalysis.Reanalysis(model=model, res=res)
  cy       = Cyclone.Cyclone(model=model, res=res)
  var_topo = ret_var_topo(model) 
  var_ua   = ret_var_ua(model) 
  var_va   = ret_var_va(model) 

  #-- const --- 
  const    = ConstCyclone.Const(model=model, res=res)
  thtopo   = const.thtopo
 
  #****************************************************
  # read lat, lon data
  #----------------------
  a1lat, a1lon = ra.Lat, ra.Lon
  ny           = ra.ny
  nx           = ra.nx
  X,Y          = meshgrid(arange(nx), arange(ny))
  #**************************************************
  # read topo data
  a2topo      = ra.load_const(var_topo).Data
  a2mask_topo = ma.masked_greater(a2topo, thtopo)
  #*************************************************
  counter = 0
  for year in range(eyear, iyear -1, -1):
    for mon in range(emon, imon -1, -1):
      print "connectc.py, down",year, mon
      ed     = calendar.monthrange(year,mon)[1]
      iDTime = datetime.datetime(year,mon,1,0)
      eDTime = datetime.datetime(year,mon,ed,24-hinc)
      lDTime = ret_lDTime(iDTime, eDTime, dDTime)[::-1]
      for DTime1 in lDTime:
        counter = counter + 1
        DTime0 = DTime1 - datetime.timedelta(hours=hinc)

        #***************************************
        #* names for 1
        #---------------------------------------
        preposname1  = cy.path_a2dat("prepos",DTime1).srcPath
        agename1     = cy.path_a2dat("age",  DTime1).srcPath

        #----------
        # read data
        #**********
        try:
          a2prepos1    = fromfile(preposname1, int32).reshape(ny,nx)
          a2age1       = fromfile(agename1,    int32).reshape(ny,nx)
        except IOError:
          counter = counter -1
          print "No File:"
          print preposname
          continue
        #**************************************
        #   inverse trace
        #--------------------------------------
        if (counter == 1):
          if flgresume == True:
            agenextname1= cy.path_a2dat("age",DTime1+datetime.timedelta(hours=hinc)).srcPath
            a2duranext   = fromfile(agenextname1, int32).reshape(ny,nx)
          else:  
            a2duranext   = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        #--------------------------
        # initialize a2dura1 and a2dura2_new
        #*****************
        a2dura1        = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        a2duranext_new = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        a2nextpos0     = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        #*****************
        ax1 = ma.masked_where(a2age1 ==miss_int, X).compressed()
        ay1 = ma.masked_where(a2age1 ==miss_int, Y).compressed()
        for iy1,ix1 in zip(ay1, ax1):
          age1    = a2age1[iy1, ix1]
          duranext = a2duranext[iy1, ix1]
          (ix0,iy0) = fortpos2pyxy(a2prepos1[iy1,ix1], nx, miss_int)
          #---- 
          if (duranext == miss_int):
            #dura1 = 1000000* age1 + int(pgmax1)
            dura1 = age1
          else:
            dura1 = duranext
          #----
          a2dura1[iy1, ix1] = dura1
          #-----------------------
          # fill a2dura2_new
          #***************
          if (ix0 != miss_int):
            a2duranext_new[iy0, ix0] = dura1
          #-----------------------
          # make "a2nextpos0"
          #***************
          if (iy0 != miss_int):
            a2nextpos0[iy0, ix0] = pyxy2fortpos(ix1, iy1, nx)


        #-------------------
        # replace a2duranext with new data
        #*******************
        a2duranext = a2duranext_new
        #**************************************
        # write to file
        #--------------------------------------
        # out dir
        #**********
        duradir1     = cy.path_a2dat("dura"   ,DTime1).srcDir
        nextposdir0  = cy.path_a2dat("nextpos",DTime0).srcDir

        mk_dir(duradir1)
        mk_dir(nextposdir0)
        #----------
        # out name
        #**********
        duraname1    = cy.path_a2dat("dura"   ,DTime1).srcPath
        nextposname0 = cy.path_a2dat("nextpos",DTime0).srcPath
        
        #----------
        # write to file
        #**********
        a2dura1.tofile(duraname1)
        a2nextpos0.tofile(nextposname0) 
        #----------
        # "nextpos" for final timestep
        #**********
        if counter == 1:
          #------
          if flgresume == True:
            preposnextname1 = cy.path_a2dat("prepos",DTime1+datetime.timedelta(hours=hinc)).srcPath
            a2preposnext1   = fromfile(preposnextname1, int32).reshape(ny,nx)
            a2nextpos1      = ones([ny,nx]*miss_int).astype(int32) 
            for iynext in range(0, ny):
              for ixnext in range(0, nx):
                if (a2preposnext1[iynext, ixnext] != miss_int):
                  (ix1,iy1) = fortpos2pyxy(a2preposnext1[iynext,ixnext], nx, miss_int)
                  a2nextpos1[iy1,ix1] = pyxy2fortpos(ixnext, iynext, nx)
          #------
          else:
            a2nextpos1    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)

          nextposdir1   = cy.path_a2dat("nextpos",DTime1).srcDir
          nextposname1  = cy.path_a2dat("nextpos",DTime1).srcPath
          mk_dir(nextposdir1)
          #------
          a2nextpos1.tofile(nextposname1)
        #----------






