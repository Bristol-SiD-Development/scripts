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
        #print >> sys.stderr, "{0} {1}".format(pdg, mcParticle.getGeneratorStatus())
        return False

def main():
    tag = None
    if len(sys.argv) < 2:
        print "Error: script requires a slcio file as input!"
        return -1

    theta_bins = np.linspace(0, np.pi, 100)

    charged_mc_bins = np.zeros_like(theta_bins)
    good_track_bins = np.zeros_like(theta_bins)


    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open( f )
	#removed_pdgs_list = []
        for event in reader:
            for trackMCTruthLink in event.getCollection("TrackMCTruthLink"):
                recoTrack = trackMCTruthLink.getFrom()
                mcParticle = trackMCTruthLink.getTo()
                if isLongLivedAndCharged(mcParticle):
                    tanLambda = getTrackParams(mcParticle, 5.)[4]
                    
                    theta = np.pi/2. - np.arctan(tanLambda)                    
                    index = np.digitize([theta], theta_bins)[0]

                    good_track_bins[index] += 1

            for particle in event.getCollection("MCParticle"):
                if isLongLivedAndCharged(mcParticle):
                    tanLambda = getTrackParams(mcParticle, 5.)[4]
                    theta = np.pi/2. - np.arctan(tanLambda)

                    index = np.digitize([theta], theta_bins)[0]
                    charged_mc_bins[index] += 1

    for theta, good_track, charged_mc in zip(theta_bins, good_track_bins, charged_mc_bins):
        print "{0} {1}".format(theta, charged_mc)

if __name__ == "__main__":
    main()
