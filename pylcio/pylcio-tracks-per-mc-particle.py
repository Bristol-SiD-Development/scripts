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

    #We use a dict because searching them is *much* faster than a list and we spend most of out time searching
    #The dict is a simple map MCParticle -> num tracks 
    #We could stick the track info in the MCParticle and just not include it in the hash but this seems simpler
    hmcp_dict = {}
    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open( f )
        for event in reader:
            for trackMCTruthLink in event.getCollection("TrackMCTruthLink"):
                #recoTrack = trackMCTruthLink.getFrom()
                mcParticle = trackMCTruthLink.getTo()
                if isLongLivedAndCharged(mcParticle):
                    hmcp = hashable_mc_particle(mcParticle)
                    try:
                        hmcp_dict[hmcp] += 1
                    except KeyError:
                        hmcp_dict[hmcp] = 0
                        
    for hmcp in hmcp_dict:  
        print "{0} {1} {2}".format(hmcp.pdg, hmcp.theta, hmcp_dict[hmcp])

if __name__ == "__main__":
    main()
