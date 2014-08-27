package org.lcsim.recon.util;

// This driver fills the vector of subdetector hit numbers for each track
// according to the convention used by ILD. At the moment this
// information is used by the LCFIPlus flavour tagging package.
//
// WARNING: This code is dependent on the detector geometry and was
// only tested for the sidloi3 model!
//
// Author: Philipp Roloff
// Last change: 18 / 06 / 2012

import java.util.List;
import java.lang.Math;

import org.lcsim.event.base.BaseTrack;
import org.lcsim.util.Driver;
import org.lcsim.event.EventHeader;
import org.lcsim.event.Track;
import org.lcsim.event.TrackerHit;
import org.lcsim.geometry.Detector;

public class TrackSubdetectorHitNumbersDriver extends Driver {

    protected String trackCollection;
    
    @Override
    protected void startOfData() {
    	trackCollection = EventHeader.TRACKS;
    }
    
    public void setTrackCollection(String trackCollection) {
		this.trackCollection = trackCollection;
	}
    
    @Override
    protected void detectorChanged(Detector detector) {
    	String name = detector.getName();
    	if (!name.equals("sidloi3")) {
    		throw new RuntimeException("The detector model "+ name +" is not supported.");
    	}
    }

    @Override
    protected void process(EventHeader event) {

	// get all tracks
	List<Track> tracks = event.get(Track.class, trackCollection);

	// loop over all tracks
	for (Track track : tracks) {

	    List<TrackerHit> hits = track.getTrackerHits();

	    // System.out.println(hits.size());

	    Integer number_vertex_barrel_hits = 0;
	    Integer number_vertex_disk_hits = 0;
	    Integer number_tracker_hits = 0;

	    // loop over all hits
	    for (TrackerHit hit : hits) {

		if (hit.getType() == 1) {
		    if (Math.abs(hit.getPosition()[2]) < 75.0) {
			number_vertex_barrel_hits++;
		    } else {
			number_vertex_disk_hits++;
		    }
		}

		if (hit.getType() == 2 || hit.getType() == 3) number_tracker_hits++;

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