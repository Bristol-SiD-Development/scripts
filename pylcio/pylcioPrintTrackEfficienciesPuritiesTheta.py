#! /bin/env python2
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from pylciohelperfunctions import *
import math
import sys

def main():
    tag = None
    if len(sys.argv) < 2:
        print >> stderr, "Error: script requires a slcio file as input!"
        return -1

    theta_bins = np.linspace(-0.1, np.pi/2. + 0.1, 40)
    good_track_bins = np.zeros_like(theta_bins)
    fake_track_bins = np.zeros_like(theta_bins)
    charged_mc_bins = np.zeros_like(theta_bins)

    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open( f )
        mcParticleCount = 0
        for i, event in enumerate(reader):
            print >> sys.stderr, i

            foundTracks, foundMcParticles =  {}, {}
            track_to_associated_mc_particles = {}
            mcParticle_to_associated_tracks = {}
            trackerHit_to_mc_particles = {}
            good_tracks = []
            fake_tracks = []

            #Find all the trackerHits and set up lists to put their mcParticles in
            for trackerHit in event.getCollection("HelicalTrackHits"):
                h_trackerHit = hashable_tracker_hit(trackerHit)
                trackerHit_to_mc_particles[h_trackerHit] = []
            
            #Loop over all the reations and append mcParticles to the list associated with their trackerHit
            for helicalTrackMCRelation in event.getCollection("HelicalTrackMCRelations"):
                mcParticle = helicalTrackMCRelation.getTo()
                trackerHit = helicalTrackMCRelation.getFrom()

                h_trackerHit = hashable_tracker_hit(trackerHit)
                h_mcParticle = hashable_mc_particle(mcParticle)

                trackerHit_to_mc_particles[h_trackerHit].append(h_mcParticle)
                
            #we call a trackerHit bad if it isn't caused by 1 mcParticle
            for trackerHit in trackerHit_to_mc_particles:
                if len(trackerHit_to_mc_particles[trackerHit]) == 1:
                    trackerHit_to_mc_particles[trackerHit] = trackerHit_to_mc_particles[trackerHit][0]
                else:
                    trackerHit_to_mc_particles[trackerHit] = None

            #Loop over all the tracks and set up lists to put their mcParticles in
            for track in event.getCollection("Tracks"):
                h_recoTrack = hashable_reco_track(track)
                track_to_associated_mc_particles[h_recoTrack] = []

            #Loop over all the mcParticle and set up lists to put their tracks in
            for mcParticle in event.getCollection("MCParticlesSkimmed"):
                if isLongLivedAndCharged(mcParticle):
                    h_mcParticle = hashable_mc_particle(mcParticle)
                    mcParticle_to_associated_tracks[h_mcParticle] = []

            #Loop over all the track <-> mcParticle relations and fill the lists
            for trackMCTruthLink in event.getCollection("TrackMCTruthLink"):
                recoTrack = trackMCTruthLink.getFrom()
                mcParticle = trackMCTruthLink.getTo()
                if isLongLivedAndCharged(mcParticle):
                    h_recoTrack = hashable_reco_track(recoTrack)
                    h_mcParticle = hashable_mc_particle(mcParticle)
                    
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
                associated_trackerHits = track.trackerHits
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


            for track in good_tracks:
                theta = math.pi/2. - math.fabs(math.pi/2. - track.getTheta())
                index = np.digitize([theta], theta_bins)
                good_track_bins[index] += 1

            for track in fake_tracks:
                theta = math.pi/2. - math.fabs(math.pi/2. - track.getTheta())
                index = np.digitize([theta], theta_bins)
                fake_track_bins[index] += 1

            for mcParticle in mcParticle_to_associated_tracks:
                theta = math.pi/2. - math.fabs(math.pi/2. - track.getTheta())
                index = np.digitize([theta], theta_bins)
                charged_mc_bins[index] += 1
                

    for theta_bin, good_track_bin, fake_track_bin, charged_mc_bin in zip(theta_bins, good_track_bins, fake_track_bins, charged_mc_bins):
        print "{0} {1} {2} {3}".format(theta_bin, good_track_bin, fake_track_bin, charged_mc_bin)


if __name__ == "__main__":
    main()
