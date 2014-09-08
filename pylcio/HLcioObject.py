import inspect
import ROOT

class NotAVectorException(Exception):
    pass
        

# Can be more fine grained by subclassing and altering hashableParams 
class HLcioObject(object):
    """Class to wrap an LCIO object. Bad things (collisions) will happen to the hash if the lcio object doesn't have enough members it understands."""

    #This stores the list of methods we consider the output of 'hashable' for each input type
    #It saves recomputing the list every time we instantiate the class
    #We just have to add an entry to the dict the first time we call the constructor on a variable of a new type
    typeHashableMethodDict = {}

    def __init__(self, lcioObject):
        self._lcioObject = lcioObject
        self.hashableParams = []
        self.hTuple = None
        self.hashValid = False

        #unfortunately we can't avoid iterating over depreciated methods
        #it doesn't really make a difference though (except all the warning messages...)


        if not type(self._lcioObject) in HLcioObject.typeHashableMethodDict:
            HLcioObject.typeHashableMethodDict[type(self._lcioObject)] = []
            for name, method in inspect.getmembers(self._lcioObject ,inspect.ismethod):
                if name[0:3] == "get" or name[0:3] == "set":
                    #want to pick up all methods which require no arguments and return types we understand (primitives and TVectors so far)
                    try:
                        t = type(method())
                        if (t == int) or (t == float) or (t == bool):
                            HLcioObject.typeHashableMethodDict[type(self._lcioObject)].append(name)
                        else:
                            try:
                                self._getTupleFromTVector(method())
                                HLcioObject.typeHashableMethodDict[type(self._lcioObject)].append(name)
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
        if not self.hashValid:
            self.hTuple = ()
            for methodName in HLcioObject.typeHashableMethodDict[type(self._lcioObject)]:
                result = self._lcioObject.__getattribute__(methodName)()
                try:
                    self.hTuple = self.hTuple + self._getTupleFromTVector(result)
                except NotAVectorException:
                    self.hTuple = self.hTuple + (result,)
            self.hashValid = True

        return self.hTuple


    def __hash__(self):
        return hash(self._getHTuple())

    def __eq__(self, other):
        try:
            return type(self._lcioObject) == type(other._lcioObject) and self._getHTuple() == other._getHTuple()
        except:
            return False
    def __ne__(self, other):
        return not (self == other)


    def __getattr__(self, name):
        if name[0:3] == "set":
            self.hashValid = False
        return self._lcioObject.__getattribute__(name)
