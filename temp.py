import Reanalysis
import Front
from numpy import *
from datetime import datetime
from front_fsub import *
import fig.Fig as Fig

front = Front.Front(model="JRA55",res="bn")
mask  = Front.Mask(model="JRA55",res="bn")
print mask.Lat
