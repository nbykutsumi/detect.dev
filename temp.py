from numpy import *
from datetime import datetime, timedelta
import detect_func
iDTime = datetime(2014,02,28,0)
eDTime = datetime(2014,3,5,0)
dDTime = timedelta(hours=6)
miss_int = -9999

def ret_lDTime(iDTime,eDTime,dDTime):
  total_steps = int( (eDTime - iDTime).total_seconds() / dDTime.total_seconds() + 1 )
  return [iDTime + dDTime*i for i in range(total_steps)]

lDTime = ret_lDTime(iDTime, eDTime, dDTime)
for DTime in lDTime:
  Year, Mon, Day, Hour = DTime.year, DTime.month, DTime.day, DTime.hour
  duraPath = "/media/disk2/out/JRA55/bn/6hr/dura/%04d/%02d/dura.%04d%02d%02d%02d.bn"%(Year,Mon,Year,Mon,Day,Hour)
  iposPath = "/media/disk2/out/JRA55/bn/6hr/ipos/%04d/%02d/ipos.%04d%02d%02d%02d.bn"%(Year,Mon,Year,Mon,Day,Hour)
  agePath  = "/media/disk2/out/JRA55/bn/6hr/age/%04d/%02d/age.%04d%02d%02d%02d.bn"%(Year,Mon,Year,Mon,Day,Hour)
  preposPath = "/media/disk2/out/JRA55/bn/6hr/prepos/%04d/%02d/prepos.%04d%02d%02d%02d.bn"%(Year,Mon,Year,Mon,Day,Hour)
  nextposPath = "/media/disk2/out/JRA55/bn/6hr/nextpos/%04d/%02d/nextpos.%04d%02d%02d%02d.bn"%(Year,Mon,Year,Mon,Day,Hour)
  a2dura   = fromfile(duraPath, int32).reshape(144,-1)
  a2ipos   = fromfile(iposPath, int32).reshape(144,-1)
  a2age    = fromfile(agePath,  int32).reshape(144,-1)
  a2prepos = fromfile(preposPath,  int32).reshape(144,-1)
  a2nextpos = fromfile(nextposPath,  int32).reshape(144,-1)

  ipos     = 21729
  dura     = ma.masked_where(a2ipos !=ipos, a2dura).compressed()
  age      = ma.masked_where(a2ipos !=ipos, a2age).compressed()
  prepos   = ma.masked_where(a2ipos !=ipos, a2prepos).compressed()
  nextpos  = ma.masked_where(a2ipos !=ipos, a2nextpos).compressed()

  prepos   = detect_func.fortpos2pyxy(prepos[0], 290, miss_int)
  nextpos   = detect_func.fortpos2pyxy(nextpos[0], 290, miss_int)

  print Mon,Day,Hour,"-->","ipos",ipos,"Age",age, "Pre",prepos,"Nxt",nextpos

