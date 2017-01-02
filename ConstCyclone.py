class Const(object):
  def __init__(self):
    self.thtopo    = 1500 # m
    self.thdura    = 36   # hours
    self.thsst     = 273.15  + 25.0  # K

    # "JRA55","bn"
    self.thpgrad = 324.0      # Pa/1000km
    self.exrvort = 3.7*1.0e-5 # s-1  lower 5.0%
    #self.exrvort = 3.3*1.0e-5 # s-1  lower 3.0%
    self.tcrvort = 3.9*1.0e-5 # s-1  lower 5.0%
    self.thwcore = 0.0        # K
