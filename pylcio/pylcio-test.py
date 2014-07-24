x#! /bin/env python

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

import sys
 
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

def print_tags(event,inputCollectionName="RefinedJets"):
    collection = event.getCollection(inputCollectionName)
    pidh = UTIL.PIDHandler(collection)
    algo = pidh.getAlgorithmID( "lcfiplus" )
    ibtag = pidh.getParameterIndex(algo, "BTag")
    ictag = pidh.getParameterIndex(algo, "CTag")
    for particle in collection:
        pid = pidh.getParticleID(particle, algo)
        print "    BTag = " + str(pid.getParameters()[ibtag])   + " CTag = " + str(pid.getParameters()[ictag])

def walk_particles(root, depth=0):
    tabs = ""
    for i in range(depth):
        tabs += "    "

    print tabs + str(root.getType()) + " " + str(root.getMass()) + " " + str(root.isCompound())
    for daughter in root.getParticles():
        walk_particles(daughter, depth+1)

def printCollectionNames(event):
    for collectionName, collection in event:
        print "collectionName: \"" + collectionName + "\", collectionTypeName: \"" + collection.getTypeName() + "\""

if __name__ == "__main__":
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    if len(sys.argv) == 2:
        print "Opening argv[1] = " + sys.argv[1]
        reader.open( sys.argv[1] )
    else:
        print "Opening default = pythiaZPolebbbar_with_particle_tbl.full.slcio" 
        reader.open( "pythiaZPolebbbar_with_particle_tbl.10.full.slcio"  )
        
    for i, event in enumerate(reader):
        # inputCollectionTypeName="ReconstructedParticle"
        #print_params(event, inputCollectionName="RefinedJets")
        #print_pids(event)
        #printCollectionNames(event)
        print "Event[" + str(i) + "]"
        print_tags(event)
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

