#! /bin/env python2
from __future__ import division
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from HelicalTrack import HelicalTrack
from FastHashableObject import FastHashableHit, FastHashableMcp, FastHashableTrack
from TrackAnalysis import TrackAnalysis

from createRootNtuples import isLongLivedAndCharged, createHitToMcpTable, createTrackToMcpTable

from RelationalTables import ManyToManyTable, ManyToOneTable

import sys
import math
import numpy as np

import pickle


def createD0ResolutionDataList(inputFileNames, num_theta_bins=100, startEvent=0):
    lcioReader = IOIMPL.LCFactory.getInstance().createLCReader()

    theta_bins = np.linspace(0, np.pi, num_theta_bins)
    d0_resolution_data = [[] for _ in xrange(num_theta_bins)]

    for fileName in inputFileNames:
        lcioReader.open(fileName)
        
        for i, event in enumerate(lcioReader):
            if i > 4999 + startEvent:
                break
            if i < startEvent:
                continue
            print >> sys.stderr, i
            

            hitToMcpTable, hTrackerHits = createHitToMcpTable(event.getCollection("HelicalTrackMCRelations"))
            
            hTracks = map(FastHashableTrack, event.getCollection("Tracks"))

            trackToMcpTable, trackToGoodHits, trackToFalseHits = createTrackToMcpTable(hTracks , hitToMcpTable)
            
            
            
            for hMcp in trackToMcpTable.toDict:
                #for each mcp in the table find its best track
                #bestTrack = None
                #nHitsBestTrack = 0
                #for hTrack in trackToMcpTable.getAllTo(hMcp):
                #    goodHits = trackToGoodHits[hTrack]
                #    if goodHits > nHitsBestTrack:
                #        nHitsBestTrack = goodHits
                #        bestHTrack = hTrack

                tracks = trackToMcpTable.getAllTo(hMcp)
                if len(tracks) == 1:
                    hTrack = tracks[0]
                    # Now get the resolution and put it in the list
                    mcHelicalTrack = HelicalTrack(inputMcp=hMcp, bField=5.)        
                    index = np.digitize([hMcp.getMomentumVec().Theta()], theta_bins)[0]
                    d0_resolution_data[index].append( mcHelicalTrack.d0 - hTrack.getD0())

            
        lcioReader.close()
    return theta_bins, d0_resolution_data

def createThetaHistogramBinList(theta_bins, d0_resolution_data):
    theta_histogram_bins_list = []
    for  theta, d0_resolution_datum in zip(theta_bins, d0_resolution_data ):
        if len(d0_resolution_datum) > 60:
            hist, bins = np.histogram(d0_resolution_datum, int(len(d0_resolution_datum)/60.))
            max_value = max(hist)
            max_index = hist.tolist().index(max_value)
            change = 1
            while change > 0:
                oldLen = len(d0_resolution_datum)
                left_cut = 0
                right_cut = -1
            
                try:
                    left_cut = hist[max_index:0].index(0, max_index, 0)
                except:
                    pass
            
                try:
                    right_cut = hist[max_index:].index(0, max_index)
                except:
                    pass

                hist, bins = np.histogram(filter(lambda x : bins[left_cut] < x < bins[right_cut], d0_resolution_datum), int(len(d0_resolution_datum)/60.))
                change = len(d0_resolution_datum) - oldLen
            theta_histogram_bins_list.append((theta, hist, bins))
        else:
            print len(d0_resolution_datum)
    return theta_histogram_bins_list

def main():
    #startEvent = int(sys.argv[1])
    outputFileName = sys.argv[1]
    #inputFileName = sys.argv[3]
    #theta_bins, d0_resolution_data = createD0ResolutionDataList([inputFileName], num_theta_bins=100, startEvent=startEvent)
    #pickle.dump((theta_bins, d0_resolution_data), open(outputFileName, "wb"))
    
    #theta_bins, d0_resolution_data = pickle.load(open(inputFileName, "rb"))


    input_file_names = sys.argv[2:]
    theta_bins, d0_resolution_data = pickle.load(open(input_file_names[0], "rb"))

    for name in input_file_names[1:]:
        for d0_resolution_datum, new_d0_resolution_datum in zip( d0_resolution_data, pickle.load(open(name, "rb"))[1]):
            d0_resolution_datum.extend(new_d0_resolution_datum)

    thetaHistogramBinList = createThetaHistogramBinList(theta_bins,d0_resolution_data)
    #print thetaHistogramBinList
    pickle.dump(thetaHistogramBinList, open(outputFileName, "wb"))




if __name__ == "__main__":
    main()
