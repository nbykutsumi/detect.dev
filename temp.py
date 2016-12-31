import IO_Master
from numpy import *
from datetime import datetime, timedelta
from detect_fsub import *

prj    = "JRA55"
model  = ""
run    = ""
res    = "145x288"

#prj    = "HAPPI"
#model  = ""
#run    = "C20-ALL-001"
#res    = ""

miss   = -9999.
iom    = IO_Master.IO_Master(prj, model, run, res)
a1lat  = iom.Lat
a1lon  = iom.Lon
ny     = iom.ny
nx     = iom.nx

DTime  = datetime(2004,1,5,0)
a2u  = iom.Load_6hrPlev("ua", DTime, 850)
a2v  = iom.Load_6hrPlev("va", DTime, 850)

a2rvort = detect_fsub.mk_a2rvort(a2u.T, a2v.T, a1lon, a1lat, miss,).T
a2rvort = ma.masked_equal(a2rvort, miss)

a  = empty([ny,nx])
a[:73] = -a2rvort[:73]
a[73:] = a2rvort[73:]
a      = ma.masked_equal(a,miss)
a      = ma.masked_equal(a,-miss)
print a
print a2rvort
