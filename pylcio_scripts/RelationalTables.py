class ManyToManyTable(object):
    def __init__(self):
        self.toDict = {}
        self.fromDict = {}

    def addRelation(self, fromObject, toObject):    
        try:
            self.toDict[toObject].append(fromObject)
        except KeyError:
            self.toDict[toObject] = [fromObject]
        try:
            self.fromDict[fromObject].append(toObject)
        except KeyError:
            self.fromDict[fromObject] = [toObject]

    def getAllFrom(self, fromObject):
        return self.fromDict.get(fromObject, [])

    def getAllTo(self, toObject):
        return self.toDict.get(toObject, [])

class ManyToOneTable(ManyToManyTable):
    def getFrom(self, fromObject):
        allFromList = super(ManyToOneTable, self).getAllFrom(fromObject)
        assert(1 == len(allFromList))
        return allFromList[0]
