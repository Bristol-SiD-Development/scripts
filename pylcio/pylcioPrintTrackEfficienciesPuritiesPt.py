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
        print >> stderr, "Error: script requires a slcio file as input!"
        return -1

    pt_max = 150
    pt_bins = np.linspace(0, pt_max, 150)

    good_track_bins = np.zeros_like(pt_bins)
    total_track_bins = np.zeros_like(pt_bins)
    charged_mc_bins = np.zeros_like(pt_bins)
    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open( f )

        for event in reader:
            foundTracks, foundMcParticles =  [], [] 
            for trackMCTruthLink in event.getCollection("TrackMCTruthLink"):
                recoTrack = trackMCTruthLink.getFrom()
                mcParticle = trackMCTruthLink.getTo()
                if isLongLivedAndCharged(mcParticle):
                    tanLambda = getTrackParams(mcParticle, 5.)[4]
                    theta = np.pi/2. - np.arctan(tanLambda)
                    if (1.5 < theta < 1.6) and (not recoTrack in foundTracks) and (not mcParticle in foundMcParticles) :
                        foundTracks.append(recoTrack)
                        foundMcParticles.append(mcParticle)
                        pt = get_track_transverse_momentum(recoTrack, 5.)
                        #pt = np.sqrt(mcParticle.getMomentum()[0]**2 + mcParticle.getMomentum()[1]**2)
                        if pt < pt_max:
                            index = np.digitize([pt], pt_bins)[0]
                            good_track_bins[index] += 1

            for track in event.getCollection("Tracks"):
                pt = get_track_transverse_momentum(track, 5.)
                theta = np.pi/2. - np.arctan(track.getTanLambda())
                if (1.5 < theta < 1.6) and pt < pt_max:
                    index = np.digitize([pt], pt_bins)[0]
                    total_track_bins[index] += 1

            for mcParticle in event.getCollection("MCParticlesSkimmed"):                
                if isLongLivedAndCharged(mcParticle):
                    theta = np.pi/2. - np.arctan(getTrackParams(mcParticle, 5.)[4])
                    if  (1.5 < theta < 1.6):
                        if pt < pt_max:
                            pt = np.sqrt(mcParticle.getMomentum()[0]**2 + mcParticle.getMomentum()[1]**2)
                            index = np.digitize([pt], pt_bins)[0]
                            charged_mc_bins[index] += 1

    for pt, good_track, total_track, charged_mc in zip(pt_bins, good_track_bins, total_track_bins, charged_mc_bins):
        print "{0} {1} {2} {3}".format(pt, good_track, total_track, charged_mc)

if __name__ == "__main__":
    main()
