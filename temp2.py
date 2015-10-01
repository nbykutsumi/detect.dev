from JRA55 import jra55
import Front
from datetime import datetime, timedelta

front = Front.front("JRA55","bn.anl_p125")

DTime = datetime(2004,3,5)
a2f   = front.load_tfront(DTime)
print a2f

