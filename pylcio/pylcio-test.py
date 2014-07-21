#! /bin/env python

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

import sys
 
# create a reader and open an LCIO file


def print_params(event, inputCollectionTypeName=None, inputCollectionName=None):
    for collectionName, collection in event:
        if ((not inputCollectionName) or collectionName == inputCollectionName) \
                and ((not inputCollectionTypeName) or collection.getTypeName() == inputCollectionTypeName):
            print "CN: " + str(collectionName) + ", CTN: " + str(collection.getTypeName())
            params =  collection.getParameters()
            for intKey in params.getIntKeys():
                print intKey + " : " + params.getIntVal(intKey)
            for floatKey in params.getFloatKeys():
                print floatKey + " : " + params.getFloatVal(floatKey)
            for stringKey in params.getStringKeys():
                print stringKey + " : " + params.getStringVal(stringKey)

def walk_particles(root, depth=0):
    tabs = ""
    for i in range(depth):
        tabs += "    "

    print tabs + str(root.getType()) + " " + str(root.getMass()) + " " + str(root.isCompound())
    for daughter in root.getParticles():
        walk_particles(daughter, depth+1)


if __name__ == "__main__":
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    if len(sys.argv) == 2:
        print "Opening argv[1] = " + sys.argv[1]
        reader.open( sys.argv[1] )
    else:
        print "Opening default = pythiaZPolebbbar_with_particle_tbl.10.full.slcio" 
        reader.open( "pythiaZPolebbbar_with_particle_tbl.10.full.slcio"  )

    for event in reader:
        # inputCollectionTypeName="ReconstructedParticle"
        print_params(event)

# loop over all events in the file
"""
for event in reader:
    print 'Content of event number %s' % ( event.getEventNumber() )


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
            
            #lInt = EVENT.StringVec()
            #lFloat = EVENT.StringVec()
            lStr = EVENT.StringVec()
            
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
   

reader.close()
"""
