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

    #theta_bins = np.linspace(0, np.pi, 100)
    #total_tracks_bins = np.zeros_like(theta_bins)
    #total_track_hits_bins = np.zeros_like(theta_bins)
    
    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open( f )
        for event in reader:            
            foundTracks = {}
            for recoTrack in event.getCollection("Tracks"):     
                tanLambda = recoTrack.getTanLambda()
                theta = np.pi/2. - np.arctan(tanLambda)
                print "{0} {1}".format(theta, len(recoTrack.getTrackerHits()))

                #index = np.digitize([theta], theta_bins)[0]
                #total_tracks_bins[index] += 1
                #total_track_hits_bins[index] += len(recoTrack.getTrackerHits())

    #for theta, total_track_hits, total_hits in zip(theta_bins, total_tracks_bins, total_track_hits_bins):
    #    print "{0} {1} {2}".format(theta, total_track_hits, total_hits)


if __name__ == "__main__":
    main()
