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

    theta_bins = np.linspace(0, np.pi, 100)

    good_track_reco_bins = np.zeros_like(theta_bins)
    good_track_mc_bins = np.zeros_like(theta_bins)
    total_track_bins = np.zeros_like(theta_bins)
    charged_mc_bins = np.zeros_like(theta_bins)
    
    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open( f )
        mcParticleCount = 0
        for i, event in enumerate(reader):
            foundTracks, foundMcParticles =  {}, {}
            for trackMCTruthLink in event.getCollection("TrackMCTruthLink"):
                recoTrack = trackMCTruthLink.getFrom()
                mcParticle = trackMCTruthLink.getTo()

                if isLongLivedAndCharged(mcParticle):
                    #hashing pyLCIO objects direcly doesn't work properly (underlying c++ may be doing something strange)
                    h_recoTrack = hashable_reco_track(recoTrack)
                    h_mcParticle = hashable_mc_particle(mcParticle)
                    if (not h_recoTrack in foundTracks) and (not h_mcParticle in foundMcParticles):
                        foundTracks[h_recoTrack] = 1
                        foundMcParticles[h_mcParticle] = 1

                        mc_tanLambda = getTrackParams(mcParticle, 5.)[4]
                        mc_theta = np.pi/2. - np.arctan(mc_tanLambda)                    
                        mc_index = np.digitize([mc_theta], theta_bins)[0]
                        good_track_mc_bins[mc_index] += 1

                        reco_tanLambda = recoTrack.getTanLambda()
                        reco_theta = np.pi/2. - np.arctan(reco_tanLambda)                    
                        reco_index = np.digitize([reco_theta], theta_bins)[0]
                        good_track_reco_bins[reco_index] += 1
            
            for track in event.getCollection("Tracks"):
                tanLambda = track.getTanLambda()
                theta = np.pi/2. - np.arctan(tanLambda)
                index = np.digitize([theta], theta_bins)[0]
                total_track_bins[index] += 1
            
            for mcParticle in event.getCollection("MCParticlesSkimmed"):
                if isLongLivedAndCharged(mcParticle):
                    mcParticleCount += 1
                    tanLambda = getTrackParams(mcParticle, 5.)[4]
                    theta = np.pi/2. - np.arctan(tanLambda)
                    index = np.digitize([theta], theta_bins)[0]
                    charged_mc_bins[index] += 1

    print >> sys.stderr, mcParticleCount
    for theta, good_track_mc, good_track_reco, total_track, charged_mc in zip(theta_bins, good_track_mc_bins, good_track_reco_bins, total_track_bins, charged_mc_bins):
        if (total_track - good_track_reco)/float(charged_mc) > 0.1:
            print >> sys.stderr, "{0} {1} {2} {3} {4}".format(theta, good_track_mc, good_track_reco, total_track, charged_mc)
        print "{0} {1} {2} {3} {4}".format(theta, good_track_mc, good_track_reco, total_track, charged_mc)


if __name__ == "__main__":
    main()
