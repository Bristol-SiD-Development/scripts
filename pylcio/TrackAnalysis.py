from __future__ import division
from HLcioObject import HLcioObject

class TrackAnalysis(object):
    def __init__(track, hitToMcRelationalTable):
        #Get the number of hits on the track
        self.nHits = len(track.getTrackerHits())

        # Create a map containing the number of hits for each MCParticle associated with the track
        mcpMap = {}

        #get the hit counts on this track for each mc particle
        for hit in track.getTrackerHits():
            hMcpList = hitToMcRelationalTable.allFromList(HLcioObject(hit))
            for hMcp in hMcpList:
                try:
                    mcMap[hMcp] += 1
                except KeyError:
                    mcMap[hMcp] = 1
                    
        # Find the MCParticle which has the most hits on the track
        nBest = 0
        hMcBest = None
        for hMcp in mcpMap:
            if mcpMap[hMcp] > nBest:
                nBest = mcpMap[hMcp]
                hMcBest = hMcp
        
        self.hMcp = hMcpBest #note that this remains None if none of the mcps has a hit

        self.nGoodHits = nBest
        self.purity = self.nGoodHits / self.nHits
        self.nBadHits = self.nHits - self.nGoodHits
