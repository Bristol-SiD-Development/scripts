#! /bin/env python

import sys
import itertools

from HLcioObject import HLcioObject

#stdout = sys.stdout
#null = open('/dev/null', 'w')

#importing these modules prints annoying stuff to the stdout...

#sys.stdout = null

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT


from pylciohelperfunctions import *

import ROOT

#and put the stdout back where we found it... 
#sys.stdout = stdout
#null.close()
# create a reader and open an LCIO file

def print_params(event, inputCollectionTypeName=None, inputCollectionName=None):
    for collectionName, collection in event:
        if ((not inputCollectionName) \
                or collectionName == inputCollectionName) \
                and ((not inputCollectionTypeName) \
                or collection.getTypeName() == inputCollectionTypeName):

            print "collectionName: " + str(collectionName) \
                + ", collectionTypeName: " \
                + str(collection.getTypeName())

            params =  collection.getParameters()

            intKeyStringVec = EVENT.StringVec()
            floatKeyStringVec = EVENT.StringVec()
            stringKeyStringVec = EVENT.StringVec()

            intValVec = EVENT.IntVec()
            floatValVec = EVENT.FloatVec()
            stringValVec = EVENT.StringVec()

            intKeys = params.getIntKeys(intKeyStringVec)
            print "Ints: "
            for intKey in intKeys:
                intVals = params.getIntVals(intKey, intValVec)
                for j, intVal in enumerate(intVals):
                    print "    " + intKey + "[" + str(j) + "]" + " ~> " + str(intVal)
            print "Floats: "
            floatKeys = params.getFloatKeys(floatKeyStringVec)
            for floatKey in floatKeys:
                floatVals = params.getFloatVals(floatKey, floatValVec)
                for j, floatVal in enumerate(floatVals):
                    print "    " + floatKey + "[" + str(j) + "]" + " ~> " + str(floatVal)
            print "Strings: "
            stringKeys = params.getStringKeys(stringKeyStringVec)
            for stringKey in stringKeys:
                stringVals = params.getStringVals(stringKey, stringValVec)
                for j, string in enumerate(stringVals):
                    print "    " + stringKey + "[" + str(j) + "]" + " ~> " + string

def print_pids(event):
    for collectionName, collection in event:
        if collection.getTypeName() == "ReconstructedParticle":
            for recon_particle in collection:
                print "Type: " + str(recon_particle.getType()) + " Goodness: " + str(recon_particle.getGoodnessOfPID())

def printCollectionNames(event):
    for collectionName, collection in event:
        print "collectionName: \"" + collectionName + "\", collectionTypeName: \"" + collection.getTypeName() + "\""

def printRecoMcTruthLinkInfo(RecoMCTruthLinkCollection):
    for RecoMCTruthLink in RecoMCTruthLinkCollection:
        recoParticle = RecoMCTruthLink.getFrom()
        mcParticle = RecoMCTruthLink.getTo()
        
        aPDG = abs(mcParticle.getPDG())
        #print "Reco mass: {0}, MC mass: {1}".format(recoParticle.getMass(), mcParticle.getMass())
        #if not (aPDG == 13 or aPDG == 22 or aPDG == 211 or aPDG == 321 or aPDG == 2112):
        print mcParticle.getPDG()

def printTrackMCTruthLinkInfo(TrackMCTruthLinkCollection):
    for TrackMCTruthLink in TrackMCTruthLinkCollection:
        print type(TrackMCTruthLink.getFrom())
        print type(TrackMCTruthLink.getTo())

def walkMcParticles(root, depth=0, max_depth=None):
    if max_depth and (depth >= max_depth):
        return False

    tabs = ""
    for i in range(0, depth):
        tabs += "     "

    momentum = []
    for i, m in enumerate(root.getMomentum()):
        if i < 3:
            momentum.append(m)
        else:
            break

    print tabs + str(root.getPDG()) + " (" + ", ".join([str(m) for m in momentum]) + ")"
    for daughter in root.getDaughters():
        walkMcParticles(daughter, depth+1,max_depth=max_depth)

    return True

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return None

if __name__ == "__main__":
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    if len(sys.argv) == 2:
        print "Opening argv[1] = " + sys.argv[1]
        reader.open( sys.argv[1] )
        """
        for event in reader:
            for collectionName, collection in event:
                for element in collection:
                    print type(element)

        """            
        #inputCollectionTypeName="ReconstructedParticle"
        #print_params(event, inputCollectionName="RecoMCTruthLink")
        #print_pids(event)
        #for event in reader:
        #    print_params(event)
        
        """
        for event in  reader:
            trackDict = {}
            for trackMcTruthLink in event.getCollection("TrackMCTruthLink"):
                htrack = HLcioObject(trackMcTruthLink.getFrom())
                try:
                    trackDict[htrack] += 1
                except KeyError:
                    trackDict[htrack] = 1

            for key in trackDict:
                if trackDict[key] != 1:
                    print trackDict[key]
                
        """

        event = reader.readNextEvent()
        mcps = event.getCollection("MCParticlesSkimmed")
        mcp = mcps.getElementAt(0)
        

        hmcp2 = HLcioObject(mcp)
        hmcp1 = HLcioObject(mcp)

        print hash(hmcp1) == hash(hmcp2)
        print hmcp1 == hmcp2
        print hmcp1 != hmcp2

        hmcp2 = HLcioObject(mcps.getElementAt(3))

        print hash(hmcp1) == hash(hmcp2)
        print hmcp1 == hmcp2
        print hmcp1 != hmcp2

        d = {hmcp1: 0, hmcp2: 1}

        for hmcpI in [hmcp1, hmcp2]:
            print d[hmcpI]
            
            
        """
        for i, event in enumerate(reader):
            print i
            mcParticles = event.getCollection("MCParticle")
            mcParticlesSkimmed = event.getCollection("MCParticlesSkimmed")
            trackMcTruthLinks  = event.getCollection("TrackMCTruthLink")

            for trackMcTruthLink in trackMcTruthLinks:
                if not trackMcTruthLink.getTo() in mcParticles:
                    print "Interesting"
                        
        """
        """
        for event in reader:
            for HelicalTrackMCRelation in event.getCollection("HelicalTrackMCRelations"):
                print type(HelicalTrackMCRelation.getFrom())
                print type(HelicalTrackMCRelation.getTo())
                break
         """
        #printTrackMCTruthLinkInfo(event.getCollection("TrackMCTruthLink"))
        #print "Event[" + str(i) + "]"
        #printRecoMcTruthLinkInfo(event.getCollection("RecoMCTruthLink"))
        #printRefinedJets_relInfo(event.getCollection("RefinedJets_rel"))
                #get_jet_flavor_from_mc(event)
        #break
        #print get_decay_product_of_interesting_mcParticle(event)
        
        #for track in event.getCollection("TrueTracks"):
        #    print "1"
        #    print track.getZ0()
            
        #break
        """
        for track in event.getCollection("Tracks"):
            covariances = track.getCovMatrix()

            counter = 0
            for i in range(0, 5):
                s = ""
                for j in range(0,i+1):
                    s += " {0}".format(covariances[counter])
                    counter += 1
                print s
        break
        """
        """
        likenesses = get_b_and_c_likenesses(event)
        actual_flavour = get_decay_product_of_interesting_mcParticle(event)

        for  likeness_dict in likenesses:
            if actual_flavour == 15 and likeness_dict["CTag"] > 0.6:
                #print  str(actual_flavour) + " " + " ".join([str(likeness_dict["BTag"]),str(likeness_dict["CTag"])])
                for mcParticle in event.getCollection("MCParticlesSkimmed"):
                    if len(mcParticle.getParents()) == 0:
                        walkMcParticles(mcParticle)
                        
                break
        """

# loop over all events in the file

"""
reader = IOIMPL.LCFactory.getInstance().createLCReader()
print "Opening argv[1] = " + sys.argv[1]
reader.open( sys.argv[1] )
for event in reader:
    print 'Content of event number %s' % ( event.getEventNumber() )
    for collectionName, collection in event:
        print collectionName

    BuildUpVertex = event.getCollection("BuildUpVertex")

    for particle in BuildUpVertex:
        print particle.getEnergy()

    primary_vertex = None
    # loop over all the collections in the event
    for collectionName, collection in event:
        if collection.getTypeName() == 'Vertex':
            for vertex in collection:
                if vertex.isPrimary():
                    print "Found primary"
                    primary_vertex = vertex                
    primary_particle = primary_vertex.getAssociatedParticle()
    walk_particles(primary_particle)

    for collectionName, collection in event:
        if collection.getTypeName() == "ReconstructedParticle":
            for recon_particle in collection:
                if recon_particle.isCompound() and recon_particle.getType() == 3:
                    params =  collection.getParameters()
                    for intKey in params.getIntKeys():
                        print intKey
                    for floatKey in params.getFloatKeys():
                        print floatKey
                    for stringKey in params.getStringKeys():
                        print stringKey
                    break

    reco_particle_collection = event.getCollection("PandoraPFOCollection")
    mc_particle_collection =  event.getCollection("MCParticle")

    print len(reco_particle_collection)
    print len(mc_particle_collection)
    for particle in mc_particle_collection:
        if particle.getPDG() == 5 or particle.getPDG() == -5: 
            print "Mass: " + str(particle.getMass()) + " Charge: " + str(particle.getCharge()) + " Type: " + str(particle.getPDG()) + "Momentum: (" + str(particle.getMomentum()[0]) + ", " + str(particle.getMomentum()[1]) + ", "+ str(particle.getMomentum()[2]) + ")" 

    for collectionName, collection in event:
        if collection.getTypeName() == "Vertex":
        #for thing in collection:
            params = collection.parameters()
            
            
            
            valStrVec = EVENT.StringVec()
            strKeys = EVENT.StringVec()

            #intKeys = params.getIntKeys(lInt)
            #floatKeys = params.getFloatKeys(lFloat)
            strKeys = params.getStringKeys(lStr)
            
            #print "Int keys len: " + str(len(intKeys))
            #print "Float keys len: " + str(len(floatKeys))
            #print "Str keys len: " + str(len(strKeys))

            for key in strKeys:
                print key
                if params.getNString(key) == 1:
                    print params.getStringVal(key) 
   
     """
reader.close()

