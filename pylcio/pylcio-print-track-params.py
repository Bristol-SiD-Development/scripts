#! /bin/env python

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

import sys

from pylciohelperfunctions import *

import itertools

def main():
    """
    Prints out a list of 15 floats for each track in each event.
    Each 15 is on a separate line
    They have the following format
    recoD0, recoPhi, recoOmega, recoZ0, recoTanLambda, recoD0Error, recoPhiError, recoOmegaError, recoZ0Error, recoTanLambdaError, MCD0, MCPhi, MCOmega, MCZ0 mcTanLambda
    """
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    if len(sys.argv) < 2:
        print "Error: script requires a slcio file as input!"
        return -1

    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open( f )

        for i, event in enumerate(reader):
            for trackMcTruthLink in event.getCollection("TrackMCTruthLink"):
                recoTrack = trackMcTruthLink.getFrom()
                mcParticle = trackMcTruthLink.getTo()
            
    
                print "{0} {1} {2} {3} {4} {5} {6}".format(recoTrack.getD0(), 
                                                           recoTrack.getPhi(), 
                                                           recoTrack.getOmega(), 
                                                           recoTrack.getZ0(), 
                                                           recoTrack.getTanLambda(),
                                                           " ".join([str(thing) for thing in getTrackParamsVariances(recoTrack)]),
                                                           " ".join([str(thing) for thing in getTrackParams(mcParticle, 5.)]))
       
        reader.close()

if __name__ == "__main__":
    main()
