#! /bin/env python2
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

#from pylciohelperfunctions import *

from HelicalTrack import HelicalTrack
from FastHashableObject import FastHashableHit, FastHashableMcp, FastHashableTrack
from TrackAnalysis import TrackAnalysis

from RelationalTables import ManyToManyTable, ManyToOneTable
from createRootNtuples import isLongLivedAndCharged, createHitToMcpTable, createTrackToMcpTable
import numpy as np
import sys
import math


def isLongLivedAndCharged(mcParticle):
    pdg =  mcParticle.getPDG() 
    if  (mcParticle.getGeneratorStatus() == 1) and ((abs(pdg) == 11) or (abs(pdg) == 13) or (abs(pdg) == 321) or (abs(pdg) == 211) or (abs(pdg) == 2212)):
        return True
    else:
        #print >> sys.stderr, "{0} {1}".format(pdg, mcParticle.getGeneratorStatus())
        return False

def main():
    startEvent=int(sys.argv[1])
    endEvent=int(sys.argv[2])

    for inputFile in sys.argv[3:]:
        lcioReader = IOIMPL.LCFactory.getInstance().createLCReader()
        lcioReader.open(inputFile)

        theta_bins = np.linspace(0, np.pi, 100)
        good_track_bins = np.zeros_like(theta_bins)
        fake_track_bins = np.zeros_like(theta_bins)

        trackCollectionName="Tracks"
        mcParticleCollectionName="MCParticlesSkimmed"
        hitMcpRelationCollectionName="HelicalTrackMCRelations"
        trackMcpRelationCollectionName="TrackMCTruthLink"
        lcioReader.skipNEvents(startEvent)
        i  = startEvent
        for event in lcioReader:
            i += 1
            if i > endEvent:
                break
            if not (startEvent < i < endEvent):
                continue
        
            print >> sys.stderr, "Event: {0}".format(event.getEventNumber())

            foundTracks, foundMcParticles =  {}, {}
            track_to_associated_mc_particles = {}
            mcParticle_to_associated_tracks = {}
            trackerHit_to_mc_particles = {}
            good_tracks = []
            fake_tracks = []

            #Find all the trackerHits and set up lists to put their mcParticles in
            for trackerHit in event.getCollection("HelicalTrackHits"):
                h_trackerHit = FastHashableHit(trackerHit)
                trackerHit_to_mc_particles[h_trackerHit] = []
            
            #Loop over all the reations and append mcParticles to the list associated with their trackerHit
            for helicalTrackMCRelation in event.getCollection("HelicalTrackMCRelations"):
                mcParticle = helicalTrackMCRelation.getTo()
                trackerHit = helicalTrackMCRelation.getFrom()

                h_trackerHit = FastHashableHit(trackerHit)
                h_mcParticle = FastHashableMcp(mcParticle)

                trackerHit_to_mc_particles[h_trackerHit].append(h_mcParticle)
                
            #we call a trackerHit bad if it isn't caused by 1 mcParticle
            for trackerHit in trackerHit_to_mc_particles:
                if len(trackerHit_to_mc_particles[trackerHit]) == 1:
                    trackerHit_to_mc_particles[trackerHit] = trackerHit_to_mc_particles[trackerHit][0]
                else:
                    trackerHit_to_mc_particles[trackerHit] = None

            #Loop over all the tracks and set up lists to put their mcParticles in
            for track in event.getCollection("Tracks"):
                h_recoTrack = FastHashableTrack(track)
                track_to_associated_mc_particles[h_recoTrack] = []

            #Loop over all the mcParticle and set up lists to put their tracks in
            for mcParticle in event.getCollection("MCParticlesSkimmed"):
                if isLongLivedAndCharged(mcParticle):
                    h_mcParticle = FastHashableMcp(mcParticle)
                    mcParticle_to_associated_tracks[h_mcParticle] = []

            #Loop over all the track <-> mcParticle relations and fill the lists
            for trackMCTruthLink in event.getCollection("TrackMCTruthLink"):
                recoTrack = trackMCTruthLink.getFrom()
                mcParticle = trackMCTruthLink.getTo()
                if isLongLivedAndCharged(mcParticle):
                    h_recoTrack = FastHashableTrack(recoTrack)
                    h_mcParticle = FastHashableMcp(mcParticle)
                    
                    track_to_associated_mc_particles[h_recoTrack].append(h_mcParticle)
                    mcParticle_to_associated_tracks[h_mcParticle].append(h_recoTrack)

            #Remove any mcParticles from the dict if they've caused more than one track
            for mcParticle in mcParticle_to_associated_tracks.keys():
                associated_tracks = mcParticle_to_associated_tracks[mcParticle]
                if len(associated_tracks) > 1:
                    mcParticle_to_associated_tracks.pop(mcParticle)

            #Good tracks are those caused by exactly one mcParticle (which in turn caused one track) and whose whose hits also have this property
            for track in track_to_associated_mc_particles:
                associated_mc_particles = track_to_associated_mc_particles[track]
                associated_mc_particles = filter(lambda mcp: mcp in mcParticle_to_associated_tracks, associated_mc_particles[:])
                
                badHits = False
                #try:

                associated_trackerHits = map(FastHashableHit, track.getTrackerHits())
                #firstHit = associated_trackerHits[0]
                
                if any( [ trackerHit_to_mc_particles[hit] == None for hit in associated_trackerHits ] ):
                    badHits = True
                else:
                    # note that the elements of a set are *unique* so this is just a cheaty way of getting the number of uniques...
                    mcParticleSet = set([trackerHit_to_mc_particles[hit] for hit in associated_trackerHits])
                    if len(mcParticleSet) > 2:
                        badHits = True                
                    
                if len(associated_mc_particles) == 1 and not badHits:
                    good_tracks.append(track)
                elif len(associated_mc_particles) > 0:
                    fake_tracks.append(track)
                #except:
                #    print >> sys.stderr, "Warning a track had no hits. Skipping..."


            for hTrack in good_tracks:
                theta = math.atan2(1., hTrack.getTanLambda())
                index = np.digitize([theta], theta_bins)
                good_track_bins[index] += 1

            for hTrack in fake_tracks:
                theta = math.atan2(1., hTrack.getTanLambda())
                index = np.digitize([theta], theta_bins)
                fake_track_bins[index] += 1

            #for mcParticle in mcParticle_to_associated_tracks:
            #    theta = math.atan2(1., HelicalTrack(inputMcp=mcParticle,bField=5.).tanL)
            #    index = np.digitize([theta], theta_bins)
            #    charged_mc_bins[index] += 1
                

    for theta_bin, good_track_bin, fake_track_bin in zip(theta_bins, good_track_bins, fake_track_bins):
        print "{0} {1} {2} {3}".format(theta_bin, good_track_bin, fake_track_bin,good_track_bin + fake_track_bin )


if __name__ == "__main__":
    main()
