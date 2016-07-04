from numpy import *
from datetime import datetime, timedelta
import Tag

model = "JRA55"
res   = "bn"
ltag = ["tc","c","fbc","ms"]

DTime = datetime(1998,9,21,0)
T     = Tag.Tag(model=model, res=res)
T.init_cyclone([1998,9],[1998,9], model=model)
dmask = T.mkMaskFrac(ltag, DTime)

dmask2=T.mkMaskFrac(ltag, DTime, ltag_2nd=["fbc"])
print dmask
