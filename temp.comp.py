from numpy import *
from detect_fsub import *
import Front
from datetime import datetime

Year   = 2004
Mon   = 6
Day   = 8
Hour  = 0
DTime = datetime(Year,Mon,Day)

new   = Front.front(model="JRA25",res="sa.one")
path_new = new.path_potloc(DTime)
srcnew1 = path_new.srcPath1
srcnew2 = path_new.srcPath2
print srcnew1
print srcnew2

srcold1 = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/%04d%02d/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Year,Mon,Day,Hour)
srcold2 = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/%04d%02d/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Year,Mon,Day,Hour)

srcrpr1 = "/media/disk2/out/JRA25/sa.one.temp2/6hr/front.t/%04d%02d/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Year,Mon,Day,Hour)
srcrpr2 = "/media/disk2/out/JRA25/sa.one.temp2/6hr/front.t/%04d%02d/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(Year,Mon,Year,Mon,Day,Hour)


a2new1 =fromfile(srcnew1,float32).reshape(180,360)
a2new2 =fromfile(srcnew2,float32).reshape(180,360)

a2old1 =fromfile(srcold1,float32).reshape(180,360)
a2old2 =fromfile(srcold2,float32).reshape(180,360)


a2rpr1 =fromfile(srcrpr1,float32).reshape(180,360)
a2rpr2 =fromfile(srcrpr2,float32).reshape(180,360)

d1 = a2new1 - a2rpr1
d2 = a2new2 - a2rpr2

print d1.max(), d1.min()
print d2.max(), d2.min()
