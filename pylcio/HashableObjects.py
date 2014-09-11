import inspect

import ROOT

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT
from array import array
import numpy as np

class FastHashableObject(object):
    def __init__(self, obj):
        self.obj = obj

        self.hashTupleValid = False
        self.hashValid = False

        self.hashTuple = self.getHTuple()
        self.hash = hash(self.hashTuple)

    def getHTuple(self):
        raise NotImplementedError()

    def _getHTuple(self):
        if not self.hashTupleValid:
            self.hTuple = self.getHTuple()
            self.hashTupleValid = True
        return self.hTuple

    def __getattr__(self, name):
        if name[0:3] == "set":
            self.hashValid = False
        return self.obj.__getattribute__(name)

    def __hash__(self):
        if not self.hashValid:
            self.hash = hash(self._getHTuple())
            self.hashValid = True
        return self.hash

    def __eq__(self, other):
        try:
            return self._getHTuple() == other._getHTuple()
        except AttributeError:
            return False   
         
    def __ne__(self, other):
        return not self == other


class FastHashableHit(FastHashableObject):
    def __init__(self, obj):
        v = obj.getPositionVec()
        self.x = v.X()
        self.y = v.Y()
        self.z = v.Z()
        super(FastHashableHit, self).__init__(obj)

    def getHTuple(self):
        return (self.obj.getEDep(), self.obj.getTime(), self.x, self.y, self.z )


class FastHashableMcp(FastHashableObject):
    def getHTuple(self):
        obj = self.obj
        p = obj.getMomentumVec()
        v = obj.getVertexVec()
        return (obj.getCharge(), obj.getMass(), p.X(), p.Y(), p.Z(), obj.getPDG(), v.X(), v.Y(), v.Z())
    
class FastHashableTrack(FastHashableObject):
    def getHTuple(self):
        obj = self.obj
        return (obj.getChi2(), obj.getD0(), obj.getdEdx(), obj.getdEdxError(), obj.getOmega(), obj.getPhi(), obj.getRadiusOfInnermostHit(), obj.getTanLambda(),  obj.getType() , obj.getZ0())
