from __future__ import division
from FastHashableObject import FastHashableHit

class TrackAnalysis(object):
    def __init__(self, track, hitToMcRelationalTable):

        hits = track.getTrackerHits()
        #Get the number of hits on the track
        self.nHits = len(hits)

        # Create a map containing the number of hits for each MCParticle associated with the track
        mcpMap = {}

        #get the hit counts on this track for each mc particle
        for hit in hits:
            hMcpList = hitToMcRelationalTable.getAllFrom(FastHashableHit(hit))
            for hMcp in hMcpList:
                try:
                    mcpMap[hMcp] += 1
                except KeyError:
                    mcpMap[hMcp] = 1
                    
        # Find the MCParticle which has the most hits on the track
        nBest = 0
        hMcpBest = None
        for hMcp in mcpMap:
            if mcpMap[hMcp] > nBest:
                nBest = mcpMap[hMcp]
                hMcpBest = hMcp
        
        self.hMcp = hMcpBest #note that this remains None if none of the mcps has a hit

        self.nGoodHits = nBest
        self.purity = self.nGoodHits / self.nHits
        self.nBadHits = self.nHits - self.nGoodHits
