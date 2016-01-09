from numpy import *
from datetime import datetime, timedelta
import Cyclone

C= Cyclone.Cyclone_2D([2010,7],[2010,8],model="JRA55",res="bn",tctype="obj")

a2tc = C.mk_a2tc(datetime(2010,8,5,12))
print a2tc.max()
