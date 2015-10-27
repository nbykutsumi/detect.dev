from numpy import *
from datetime import datetime
import detect_func
import calendar
import Cyclone

#-- test @ 27 Oct --
iYear = 2010
eYear = 2014
lYear = range(iYear,eYear+1)
lMon  = range(1,12+1)
lHour = [0,6,12,18]

model  = "JRA55"
res    = "bn"
#tctype = "obj"
tctype = "bst"
radkm  = 1000.

for Year in lYear:
  for Mon in lMon:
    #--- init ----
    Cy   = Cyclone.Cyclone_2D(Year,Mon,model=model, res=res, tctype=tctype)
    #-------------
    iDay = 1
    eDay = calendar.monthrange(Year,Mon)[1]
    for Day,Hour in [[Day,Hour] for Day in range(iDay, eDay+1) for Hour in lHour]:
      DTime = datetime(Year,Mon,Day,Hour)
            
      a2exc = Cy.mkMask_exc(DTime, radkm=radkm) 
      a2tc  = Cy.mkMask_tc (DTime, radkm=radkm)

      oDir_exc, oPath_exc = Cy.path_Mask_exc(DTime)
      oDir_tc,  oPath_tc  = Cy.path_Mask_tc (DTime)

      detect_func.mk_dir(oDir_exc)
      detect_func.mk_dir(oDir_tc )

      a2exc.tofile(oPath_exc)
      a2tc .tofile(oPath_tc)
      print oPath_exc



