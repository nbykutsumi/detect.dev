import IO_Master
from datetime import datetime, timedelta

prj    = "JRA55"
model  = ""
run    = ""
res    = "bn"

#prj    = "HAPPI"
#model  = ""
#run    = "C20-ALL-001"
#res    = ""

iom    = IO_Master.IO_Master(prj, model, run, res)

var    = "ta"
plev   = 500

lat = iom.Lat
slat="\n".join(map(str,lat)).strip()
print slat
