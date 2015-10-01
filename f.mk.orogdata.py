from numpy import *
from detect_fsub import *
import Reanalysis
import Front
import fig.Fig as Fig

calcflag  = True
#calcflag  = False
model = "JRA25"
#model = "JRA55"
res   = "bn"
radkm = 300.  # (km)

ra    = Reanalysis.Reanalysis(model=model, res=res)
ny    = ra.ny
nx    = ra.nx
a1lat = ra.Lat 
a1lon = ra.Lon
miss  = -9999.

orog       = ra.load_const("topo")
oDir       = orog.srcDir
maxorogname= oDir + "/maxtopo.%04dkm.%s"%(radkm, res)

if calcflag==True:
  a2orog     = orog.load_const("topo").Data 
  a2maxorog  = detect_fsub.mk_a2max_rad(a2orog.T, a1lon, a1lat, radkm, miss).T
  #--- write to file -------
  a2maxorog.tofile(maxorogname)

#--- figure: max orog ----
figname = maxorogname + ".png"
Fig.DrawMap( a2maxorog, a1lat, a1lon, figname=figname)
