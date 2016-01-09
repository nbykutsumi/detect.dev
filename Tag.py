from numpy import *
from datetime import datetime
import Cyclone
import Front
import ConstMask
import sys

class Tag(ConstMask.Const):
  def __init__(self, model="JRA55", res="bn", miss=-9999.):

    ConstMask.Const.__init__(self, model, res)

    self.model = model
    self.res   = res
    self.miss  = miss
    self.Front = Front.Front(model, res, miss)

  #def init_cyclone(self, Year, Mon, tctype="bst"):
  #  """
  #  tctype: "obj", "bst"
  #  """
  #  self.Cyclone = Cyclone.Cyclone_2D(Year, Mon, tctype=tctype, miss=self.miss)
  #  return self

  def init_cyclone(self, iYM, eYM, model="JRA55", tctype="bst"):
    """
    tctype: "obj", "bst"
    """
    self.Cyclone = Cyclone.Cyclone_2D(iYM, eYM, model=model, tctype=tctype, miss=self.miss)
    return self



  def mkMask(self, tag, DTime, radkm=False, miss=False):
    """
    tags:
    "tc"
    "c"
    "fbc" or "front.t"
    "nbc" or "front.q"
    """
    if type(miss) == bool: miss = self.miss

    if tag in ["fbc","front.t"]:
      if type(radkm)==bool: radkm = self.dictRadkm[tag]
      return self.Front.mkMask_tfront(DTime=DTime, radkm=radkm, miss=miss)

    elif tag in ["nbc","front.q"]:
      if type(radkm)==bool: radkm = self.dictRadkm[tag]
      return self.Front.mkMask_qfront(DTime=DTime, radkm=radkm, miss=miss)

    elif tag == "tc":
      if type(radkm)==bool: radkm = self.dictRadkm[tag]
      return self.Cyclone.mkMask_tc(DTime=DTime, radkm=radkm, miss=miss)

    elif tag == "c":
      if type(radkm)==bool: radkm = self.dictRadkm[tag]
      return self.Cyclone.mkMask_exc(DTime=DTime, radkm=radkm, miss=miss)

    elif tag == "cf":
      if type(radkm) != bool:
        print "Tag.py: radkm cannot be specified for combinations";sys.exit()
      a2c = self.Cyclone.mkMask_exc(DTime=DTime, radkm=self.dictRadkm["c"], miss=miss)
      a2f = self.Front.mkMask_tfront(DTime=DTime, radkm=self.dictRadkm["fbc"], miss=miss)
      return ma.masked_where(a2c != miss, a2f).filled(1.0)

    else:
      print "check! tag=",tag
      sys.exit()

#  def mkMask_wgt(self, ltag, DTime, miss=0.0):
#    """
#    ltag = ["tag1", "tag2", ...], without "ot"
#    """
#    dictMask = {}
#
#    for tag in ltag:
#      dictMask[tag] = self.mkMask(tag, DTime, miss=0.0)
#     
#    a2sum    = array([dictMask[tag] for tag in ltag]).sum(axis=0)
#    a2denomi = ma.masked_equal(a2sum, 0.0).filled(1.0)
#
#    for tag in ltag:
#      dictMask[tag] = dictMask[tag] / a2denomi
#
#    #- ot --
#    dictMask["ot"] = ma.masked_where(a2sum >0.0, ones(a2sum.shape, float32)).filled(miss)
#
#    #-- miss --
#    if miss != 0.0:
#      for tag in ltag: 
#        dictMask[tag] = ma.masked_equal(dictMask[tag], 0.0).filled(miss)
#    #----------
#    return dictMask

  def mkMaskFrac(self, ltag, DTime, miss=0.0):
    """
    ltag = ["tag1", "tag2", ...], without "ot"
    """
    dictMask = {}
    for tag in ltag:
      dictMask[tag] = self.mkMask(tag, DTime, miss=0.0)
     
    return self.mkMaskFracCore(dictMask, miss)


  def mkMaskFracCore(self, dictMask=False, miss=0.0):
    ltag     = dictMask.keys()
    a2sum    = array([dictMask[tag] for tag in ltag]).sum(axis=0)
    a2denomi = ma.masked_equal(a2sum, 0.0).filled(1.0)

    dictMaskFrac = {}
    for tag in ltag:
      dictMaskFrac[tag] = dictMask[tag] / a2denomi

    #- ot --
    dictMaskFrac["ot"] = ma.masked_where(a2sum >0.0, ones(a2sum.shape, float32)).filled(miss)

    #-- miss --
    if miss != 0.0:
      for tag in ltag: 
        dictMaskFrac[tag] = ma.masked_equal(dictMaskFrac[tag], 0.0).filled(miss)
    #----------
    return dictMaskFrac

 
