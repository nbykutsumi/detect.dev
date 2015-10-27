from numpy import *
from datetime import datetime
import Front
import detect_func
import calendar


model  = "JRA55"
res    = "bn"
iYear  = 2015
#eYear  = 2010
eYear  = 2015
lYear  = range(iYear, eYear+1)
lMon   = range(1,12+1)
lHour  = [0,6,12,18]
#lHour  = [0]

F  = Front.Front(model=model, res=res)

for Year in lYear:
  for Mon in lMon:
    iDay  = 1
    eDay  = calendar.monthrange(Year, Mon)[1]
    for Day, Hour in [[Day,Hour] for Day in range(iDay, eDay+1) for Hour in lHour]:
      DTime    = datetime(Year,Mon,Day,Hour)
      oDir_t, oPath_t = F.path_finloc(DTime, tq="t")
      oDir_q, oPath_q = F.path_finloc(DTime, tq="q")

      loc_t  = F.mk_tfront(DTime)
      loc_q  = F.mk_qfront(DTime)

      detect_func.mk_dir(oDir_t)
      detect_func.mk_dir(oDir_q)

      loc_t.tofile(oPath_t)
      loc_q.tofile(oPath_q)
      print oPath_t



