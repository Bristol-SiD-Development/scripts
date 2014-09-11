#! /bin/env python2
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from pylciohelperfunctions import *

import sys

def isLongLivedAndCharged(mcParticle):
    pdg =  mcParticle.getPDG() 
    if  (mcParticle.getGeneratorStatus() == 1) and ((abs(pdg) == 11) or (abs(pdg) == 13) or (abs(pdg) == 321) or (abs(pdg) == 211) or (abs(pdg) == 2212)):
        return True
    else:
        return False

def main():
    tag = None
    if len(sys.argv) < 2:
        print >> stderr, "Error: script requires a slcio file as input!"
        return -1

    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    for f in sys.argv[1:]:
        reader.open( f )
        for i, event in enumerate(reader):
            for track in event.getCollection("Tracks"):
                print get_track_transverse_momentum(track, 5.)

        reader.close()
            
if __name__ == "__main__":
    main()
