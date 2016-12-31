class Const(object):
  def __init__(self):
    self.thtopo    = 1500 # m
    self.thdura    = 48   # hours
    self.thsst     = 273.15  + 25.0  # K

    # "JRA55","bn"
    self.thpgrad = 324.0      # Pa/1000km
    self.exrvort = 3.7*1.0e-5 # s-1 tuned@2016/12/31
    self.tcrvort = 3.5*1.0e-5 # s-1
    self.thwcore = 0.0        # K
