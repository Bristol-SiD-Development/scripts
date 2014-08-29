package org.lcsim.recon.util;

// This driver fills the vector of subdetector hit numbers for each track
// according to the convention used by ILD. At the moment this
// information is used by the LCFIPlus flavour tagging package.
//
// WARNING: This code is dependent on the detector geometry and was
// only tested for the sidloi3 model!
//
// Specifically it requires the "SiVertexEndcap" and "SiVertexBarrel" to be present
// It will almost certainly do the wrong thing if your detector is too unlike sidloi3
//
// Changed by Oliver Reardon-Smith
// Last change 29/08/2014
//
// Author: Philipp Roloff

import java.util.List;
import java.util.Map;
import java.util.Set;

import java.util.logging.Level;

import hep.physics.vec.Hep3Vector;
import hep.physics.vec.BasicHep3Vector;

import org.lcsim.event.base.BaseTrack;
import org.lcsim.util.Driver;

import org.lcsim.event.EventHeader;
import org.lcsim.event.Track;
import org.lcsim.event.TrackerHit;
import org.lcsim.event.RawTrackerHit;

import org.lcsim.geometry.Detector;
import org.lcsim.geometry.compact.Subdetector;

import org.lcsim.detector.IDetectorElement;

public class TrackSubdetectorHitNumbersDriver extends Driver {

    protected String trackCollection;
    protected IDetectorElement siVertexEndcapIDetectorElement;
    protected IDetectorElement siVertexBarrelIDetectorElement;
    protected IDetectorElement siTrackerForwardIDetectorElement;

    @Override
    protected void startOfData() {
        trackCollection = EventHeader.TRACKS;
    }

    public void setTrackCollection(String trackCollection) {
        this.trackCollection = trackCollection;
    }

    @Override
    protected void detectorChanged(Detector detector) {

        Set<String> subDetectorNames = detector.getSubdetectorNames();

        if( !(subDetectorNames.contains("SiVertexEndcap") && subDetectorNames.contains("SiTrackerForward") && subDetectorNames.contains("SiVertexBarrel")) ){
            throw new RuntimeException("The detector must contain subdetectors named SiVertexBarrel, SiVertexEndcap and SiTrackerForward otherwise the \"" + this.getName() + "\" driver will fail.");
        }

        Subdetector siVertexEndcapSubdetector = detector.getSubdetector("SiVertexEndcap");
        Subdetector siTrackerForwardSubdetector = detector.getSubdetector("SiTrackerForward");
	Subdetector siVertexBarrelSubdetector = detector.getSubdetector("SiVertexBarrel");
	
        this.siVertexEndcapIDetectorElement = siVertexEndcapSubdetector.getDetectorElement();
        this.siTrackerForwardIDetectorElement = siTrackerForwardSubdetector.getDetectorElement();
	this.siVertexBarrelIDetectorElement = siVertexBarrelSubdetector.getDetectorElement();
    }

    @Override
    protected void process(EventHeader event) {

        // get all tracks
        List<Track> tracks = event.get(Track.class, trackCollection);

	// loop over all tracks
        for (Track track : tracks) {
            List<TrackerHit> hits = track.getTrackerHits();

            Integer number_vertex_barrel_hits = 0;
            Integer number_vertex_disk_hits = 0;
            Integer number_tracker_hits = 0;

            // loop over all hits
            for (TrackerHit hit : hits) {
                if (hit.getType() == 1) {
		    Hep3Vector hitPosition = new BasicHep3Vector(hit.getPosition());
		    
		    List<RawTrackerHit> rawTrackerHits = hit.getRawHits();

		    if(rawTrackerHits.size() < 1){
			throw new RuntimeException("A tracker hit was encountered with no raw tracker hits associated");
		    }

		    RawTrackerHit firstRawTrackerHit = rawTrackerHits.get(0);
		    IDetectorElement trackerHitIDetectorElement = firstRawTrackerHit.getDetectorElement();

		    if( this.siVertexBarrelIDetectorElement.isDescendant(trackerHitIDetectorElement) ){
                        number_vertex_barrel_hits++;
                    }
		    else  if( this.siVertexEndcapIDetectorElement.isDescendant(trackerHitIDetectorElement) ){
                        number_vertex_disk_hits++;
                    }
		    else if (this.siTrackerForwardIDetectorElement.isDescendant(trackerHitIDetectorElement)){ //for some reason tracker forward hits come labelled with 1
			number_tracker_hits++;
		    }else{
			this.getLogger().log(Level.WARNING, "A vertex detector hit was found not in the vertex barrel, not in the vertex endcap and not in the tracker forward. This is probably a problem.");
		    }
                }
		else if(hit.getType() == 2 || hit.getType() == 3){
		    number_tracker_hits++;
		} 

            } // end loop over all hits

            int[] subdetector_hits;
            subdetector_hits = new int[12];

            // fill hit numbers in ILD style array
            subdetector_hits[0] = number_vertex_barrel_hits; // "VTX"
            subdetector_hits[1] = number_vertex_disk_hits; // "FTD"
            subdetector_hits[2] = 0; // "SIT"
            subdetector_hits[3] = number_tracker_hits; // "TPC"
            subdetector_hits[4] = 0; // "SET"
            subdetector_hits[5] = 0; // "ETD"
            subdetector_hits[6] = number_vertex_barrel_hits; // "VTX"
            subdetector_hits[7] = number_vertex_disk_hits; // "FTD"
            subdetector_hits[8] = 0; // "SIT"
            subdetector_hits[9] = number_tracker_hits; // "TPC"
            subdetector_hits[10] = 0; // "SET"
            subdetector_hits[11] = 0; // "ETD"

            ((BaseTrack)track).setSubdetectorHitNumbers(subdetector_hits);
        }

    }
}