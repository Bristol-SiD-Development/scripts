import inspect
import ROOT

class NotAVectorException(Exception):
    pass
        

# Can be more fine grained by subclassing and altering hashableParams 
class HLcioObject(object):
    """Class to wrap an LCIO object. Bad things (collisions) will happen to the hash if the lcio object doesn't have enough members it understands."""
    def __init__(self, lcioObject):
        self.lcioObject = lcioObject
        self.hashableParams = []        
        #unfortunately we can't avoid iterating over depreciated methods
        #it doesn't really make a difference though (except all the warning messages...)

        for name, method in inspect.getmembers(self.lcioObject ,inspect.ismethod):
            if name[0:3] == "get" or name[0:3] == "set":
                self.__dict__[name] = method
                #want to pick up all methods which require no arguments and return types we understand (primitives and TVectors so far)
                try:
                    t = type(method())
                    if (t == int) or (t == float) or (t == bool):
                        self.hashableParams.append( method)
                    else:
                        try:
                            self._getTupleFromTVector(method())
                            self.hashableParams.append(method)
                        except NotAVectorException:
                            continue
                except TypeError: #TypeError is thrown when we call a method without all the parameters it requires
                    continue

    def _getTupleFromTVector(self, v): #physics vectors
        tup = ()
        if type(v) == ROOT.TVector2:
            return (v.X(), v.Y())
        elif type(v) == ROOT.TVector3:
            return (v.X(), v.Y(), v.Z())
        elif type(v) == ROOT.TLorentzVector:
            return (v.X(), v.Y(), v.Z(), v.T())
        try:
            tup = tup + (v.X())
        except:
            pass
        try:
            tup = tup + (v.Y())
        except:
            pass
        try:
            tup = tup + (v.Z())
        except:
            pass
        try:
            tup = tup + (v.T())
        except:
            pass

        if tup == ():
            raise NotAVectorException("A physics vector must implement one of v.X, v.Y, v.Z or v.T")

        return tup

    def _getHTuple(self):
        #unfortunately we can't avoid iterating over depreciated methods
        #it doesn't really make a difference though
        hTuple = ()
        for method in self.hashableParams:
            try:
                hTuple = hTuple + self._getTupleFromTVector(method())
            except NotAVectorException:
                hTuple = hTuple + (method(),)
        return hTuple

    def __hash__(self):
        return hash(self._getHTuple())

    def __eq__(self, other):
        try:
            return type(self.lcioObject) == type(other.lcioObject) and self._getHTuple() == other._getHTuple()
        except:
            return False
    def __ne__(self, other):
        return not (self == other)
