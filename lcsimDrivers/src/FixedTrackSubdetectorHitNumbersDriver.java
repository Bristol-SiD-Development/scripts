//package org.lcsim.recon.util;

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
import java.util.Map;
import java.util.Set;

import java.lang.Math;

import org.lcsim.event.base.BaseTrack;
import org.lcsim.util.Driver;

import org.lcsim.event.EventHeader;
import org.lcsim.event.Track;
import org.lcsim.event.TrackerHit;

import org.lcsim.geometry.Detector;
import org.lcsim.geometry.compact.Subdetector;

import org.lcsim.detector.IGeometryInfo;
import org.lcsim.detector.IDetectorElement;

import org.lcsim.detector.solids.Inside;

public class FixedTrackSubdetectorHitNumbersDriver extends Driver {

    protected String trackCollection;
    protected IGeometryInfo siVertexEndcapIGeometryInfo;
    protected IGeometryInfo siVertexBarrelIGeometryInfo;

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

        if( !(subDetectorNames.contains("SiVertexEndcap") && subDetectorNames.contains("SiVertexBarrel")) ){
            throw new RuntimeException("The detector must contain subdetectors named SiVertexBarrel and SiVertexEndcap otherwise the \"" + this.getName() + "\" driver will fail.");
        }

        Subdetector siVertexEndcapSubdetector = detector.getSubdetector("SiVertexEndcap");
        Subdetector siVertexBarrelSubdetector = detector.getSubdetector("SiVertexBarrel");

        IDetectorElement siVertexEndcapIDetectorElement = siVertexEndcapSubdetector.getDetectorElement();
        IDetectorElement siVertexBarrelIDetectorElement = siVertexBarrelSubdetector.getDetectorElement();

        this.siVertexEndcapIGeometryInfo = siVertexEndcapIDetectorElement.getGeometry();
        this.siVertexBarrelIGeometryInfo = siVertexBarrelIDetectorElement.getGeometry();
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

            Hep3Vector hitPosition;
            Inside insideSiVertexEndcap;
            Inside insideSiVertexBarrel;

            // loop over all hits
            for (TrackerHit hit : hits) {
                if (hit.getType() == 1) {
                    hitPosition = Hep3Vector(hit.getPosition());
                    insideSiVertexEndcap = this.siVertexEndcapIGeometryInfo.inside(hitPosition);
                    insideSiVertexBarrel = this.siVertexBarrelIGeometryInfo.inside(hitPosition);

                    //It is posible (in simulated events) for a hit to be inside both the endcap and the vertex barrel if they intersect
		    //This code assumes the hits were in the barrel if this happens.
		    if( (insideSiVertexBarrel == Inside.INSIDE) || (insideSiVertexBarrel == Inside.SURFACE) ){
                        number_vertex_barrel_hits++;
			if( (insideSiVertexEndcap == Inside.INSIDE) || (insideSiVertexEndcap == Inside.SURFACE) ){
			    System.out.println("Warning: A vertex detector hit was found in both the barrel and the endcap. The barrel count was incremented.")
			}
                    }
		    else  if( (insideSiVertexEndcap == Inside.INSIDE) || (insideSiVertexEndcap == Inside.SURFACE) ){
                        number_vertex_disk_hits++;
                    }
		    else{
			System.out.println("Warning: A vertex detector hit was found not in the vertex barrel and not in the vertex endcap. This probably indicates a fairly major problem.");
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