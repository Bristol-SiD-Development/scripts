#! /bin/env python2
import ROOT

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from pylciohelperfunctions import HelicalTrack, isLongLivedAndCharged

from HLcioObject import HLcioObject
from TrackAnalysis import TrackAnalysis
from array import array

import sys

import numpy as np

class ManyToManyTable(object):
    def __init__(self):
        self.toDict = {}
        self.fromDict = {}
        #self.relationList = []
    def addFrom(self, fromObject):
        if not fromObject in self.fromDict:
            self.fromDict[fromObject] = []
    def addTo(self, toObject):
        if not toObject in self.toDict:
            self.toDict[toObject] = []

    def addRelation(self, fromObject, toObject):
        self.addFrom(fromObject)
        self.addTo(toObject)

        self.toDict[toObject].append(fromObject)
        self.fromDict[fromObject].append(toObject)
        #self.relationList.append((fromObject, toObject))

    def getAllFrom(self, fromObject):
        return self.fromDict.get(fromObject, [])

    def getAllTo(self, toObject):
        return self.toDict.get(toObject, [])
    #def getAllrelations(self):
    #    return self.relationsList

class ManyToOneTable(ManyToManyTable):
    def getFrom(self, fromObject):
        allFromList = super(ManyToOneTable, self).getAllFrom(fromObject)
        assert(1 == len(allFromList))
        return allFromList[0]

def convTheta(theta):
    return 90. - 180.*abs(theta/np.pi - 0.5)

def getBucketDict():
    bucketDict = {"event": ('I',  array('i', [0])), #done
                  "Ntracks": ('I', array('i', [0])), #done 
                  "nMCPs": ('I', array('i', [0])), #done
                  "track_nHits":['int', 'track'], #done
                  "track_nFalseHits":['int','track'], #done
                  "track_d0":['double','track'], #done
                  "track_z0":['double','track'], #done
                  "track_dca":['double','track'], #done
                  "track_px":['double','track'], #done
                  "track_py":['double','track'], #done
                  "track_pz":['double','track'], #done
                  "track_pt":['double','track'], #done
                  "track_p":['double','track'], #done
                  "track_theta":['double','track'], #done
                  "track_theta_conv":['double','track'], #done
                  "track_phi":['double','track'], #done
                  "track_charge":['int','track'], #done
                  "track_sigma_d0":['double','track'], #done
                  "track_sigma_z0":['double','track'], #done
                  "track_sigma_dca":['double','track'], #done
                  "track_sigma_px":['double','track'], #done
                  "track_sigma_py":['double','track'], #done
                  "track_sigma_pz":['double','track'], #done
                  "track_sigma_pt":['double','track'], #done
                  "track_sigma_p":['double','track'], #done
                  "track_sigma_theta":['double','track'], #done
                  "track_sigma_theta_conv":['double','track'], #done
                  "track_sigma_phi":['double','track'], #done
                  "track_mc_nHits":['int','track'], #done 
                  "track_mc_d0":['double','track'], #done
                  "track_mc_z0":['double','track'], #done
                  "track_mc_dca":['double','track'], #done
                  "track_mc_x":['double','track'], #done
                  "track_mc_y":['double','track'], #done
                  "track_mc_z":['double','track'], #done
                  "track_mc_d_origin":['double','track'], #done
                  "track_mc_px":['double','track'], #done
                  "track_mc_py":['double','track'], #done
                  "track_mc_pz":['double','track'], #done
                  "track_mc_pt":['double','track'], #done
                  "track_mc_p":['double','track'], #done
                  "track_mc_theta":['double','track'], #done
                  "track_mc_theta_conv":['double','track'], #done
                  "track_mc_phi":['double','track'], #done
                  "track_mc_pathlength":['double','track'], #done (ish)
                  "track_mc_pathlength_los":['double','track'], #done (ish)
                  "track_mc_distance":['double','track'], #done
                  "track_mc_charge":['double','track'], #done
                  "track_mc_pdgid":['int','track'], #done
                  "track_mc_signal":['int','track'], #done (ish)
                  "track_mc_status":['int','track'], #done (ish)
                  "track_mc_findable":['int','track'], #done (isn)
                  "track_mc_besttrack":['int','track'], #done
                  "mc_nHits":['int', "mcp"], #done
                  "mc_d0":['double', "mcp"], #done
                  "mc_z0":['double', "mcp"], #done
                  "mc_dca":['double', "mcp"], #done
                  "mc_x":['double', "mcp"], #done
                  "mc_y":['double', "mcp"], #done
                  "mc_z":['double', "mcp"], #done
                  "mc_d_origin":['double', "mcp"], #done
                  "mc_px":['double', "mcp"], #done
                  "mc_py":['double', "mcp"], #done
                  "mc_pz":['double', "mcp"], #done
                  "mc_pt":['double', "mcp"], #done
                  "mc_p":['double', "mcp"], #done
                  "mc_theta":['double', "mcp"], #done
                  "mc_theta_conv":['double', "mcp"], #done
                  "mc_phi":['double', "mcp"], #done
                  "mc_pathlength":['double', "mcp"], #done (ish)
                  "mc_pathlength_los":['double', "mcp"], #done (ish)
                  "mc_distance":['double', "mcp"], #done
                  "mc_charge":['double', "mcp"], #done
                  "mc_pdgid":['int', "mcp"], #done
                  "mc_signal":['int', "mcp"], #done (ish)
                  "mc_status":['int', "mcp"], #done
                  "mc_findable":['int', "mcp"], #done (ish)
                  "mc_reconstructed":['int', "mcp"]} #done
    #TODO come up with a good way of distinguishing scalar and vector params
    for key in bucketDict:
        if type(bucketDict[key]) == list:
            bucketDict[key].append(ROOT.vector(bucketDict[key][0])(0))

    return bucketDict

def createRootFile(inputLcioFile, rootOutputFile, bField=5., 
                   trackCollectionName="Tracks", 
                   mcParticleCollectionName="MCParticlesSkimmed", 
                   hitMcpRelationCollectionName="HelicalTrackMCRelations",
                   trackMcpRelationCollectionName="TrackMCTruthLink"):
    lcioReader = IOIMPL.LCFactory.getInstance().createLCReader()
    lcioReader.open(inputLcioFile)

    f = ROOT.TFile(rootOutputFile, "RECREATE")
    tree = ROOT.TTree('aTree', 'stillATree')

    bucketDict = getBucketDict()
    #implementedKeys = ["event", "Ntracks", "nMCPs", "mc_x", "mc_y", "mc_z", "mc_px", "mc_py", "mc_pz", "mc_pt", "mc_p", "mc_d0", "mc_z0","mc_dca", "mc_theta", "mc_phi"]
    for key in bucketDict:
        if type(bucketDict[key]) == list: #The vector parameters have their buckets in lists so we can mutate them (need to create new vectors)
            tree.Branch(key, bucketDict[key][2])
        elif type(bucketDict[key]) == tuple: #The scalars (length one arrays) go in tuples as we don't need to mutate the array only the contents
            tree.Branch(key, bucketDict[key][1], "{0}/{1}".format(key, bucketDict[key][0]))
        else:
            raise Exception("My hovercraft is full of eels")

    for event in lcioReader:
        bucketDict["event"][1][0] = event.getEventNumber()
        tracks = event.getCollection(trackCollectionName)
        bucketDict["Ntracks"][1][0] = tracks.getNumberOfElements()
        mcParticles = event.getCollection(mcParticleCollectionName)
        bucketDict["nMCPs"][1][0] = mcParticles.getNumberOfElements()

        hitMcpRelations = event.getCollection(hitMcpRelationCollectionName)
        trackMcpRelations = event.getCollection(trackMcpRelationCollectionName)

        for key in bucketDict:
            if type(bucketDict[key]) == list:
                length = None
                if bucketDict[key][1] == "track":
                    length = tracks.getNumberOfElements()
                elif bucketDict[key][1] == "mcp":
                    length = mcParticles.getNumberOfElements()
                else:
                    raise Exception("WTF is this shit?!")

                bucketDict[key][2] = ROOT.vector(bucketDict[key][0])()
                bucketDict[key][2].resize(length)
                tree.SetBranchAddress(key, bucketDict[key][2])

        #Create a table relating hits to mcParticles and a list of all the hTrackerHits
        hitToMcpTable = ManyToManyTable()
        hTrackerHits = []
        for hitMcpRelation in hitMcpRelations:
            hHit = HLcioObject(hitMcpRelation.getFrom())
            hMcp = HLcioObject(hitMcpRelation.getTo())
            
            hitToMcpTable.addRelation(hHit, hMcp)

            if not hHit in hTrackerHits:
                hTrackerHits.append(hHit)
                
        #build a map of track to (best) MCParticle
        #Note that the same MCParticle can be best for many tracks
        trackToMcpTable = ManyToOneTable()
        trackToGoodHits = {}
        trackToFalseHits = {}
        for trackMcpRelation in trackMcpRelations:
            hTrack = HLcioObject(trackMcpRelation.getFrom())
            trackAnalysis = TrackAnalysis(hTrack, hitToMcpTable)

            trackToMcpTable.addRelation(hTrack, trackAnalysis.hMcp)

            trackToGoodHits[hTrack] = trackAnalysis.nGoodHits
            trackToFalseHits[hTrack] = trackAnalysis.nBadHits

        
        # For each hit find the distance to the nearest other hit
        distanceToNearestHit = {}
        for hHit in hTrackerHits:
            for otherHHit in hTrackerHits:
                if hHit != otherHHit:
                    hitPos = hHit.getPositionVec()
                    otherHitPos = otherHHit.getPositionVec()
                    distance = (hitPos - otherHitPos).Mag()

                    try:
                        if distance < distanceToNearestHit[hHit]:
                            distanceToNearestHit[hHit] = distance
                    except KeyError:
                        distanceToNearestHit[hHit] = distance


        #Create a list of all the long lived and charged MCParticles
        longLivedAndChargedHMcParticles = []
        for mcp in mcParticles:
            if isLongLivedAndCharged(mcp):
                longLivedAndChargedHMcParticles.append(HLcioObject(mcp))

        
        #For each MCParticle find the shortest distance between any of its hits and any other hit
        mcDistance = {}
        for mcp in mcParticles:
            hMcp = HLcioObject(mcp)
            hHits = hitToMcpTable.getAllTo(hMcp)
            
            for hHit in hHits:
                minDistance = sys.float_info.max
                if hHit in distanceToNearestHit:
                    minDistance = distanceToNearestHit[hHit]
                try:
                    if minDistance < mcDistance[hMcp]:
                        mcDistance[hMcp] = minDistance
                except KeyError:
                    mcDistance[hMcp] = minDistance
                

        reconstructedMcps = [] 
        for trackIndex, track in enumerate(tracks):
            hTrack = HLcioObject(track)
            recoHMcp = trackToMcpTable.getFrom(hTrack)
            
            reconstructedMcps.append(recoHMcp)
            
            #check if this is the best track for our reco MCP
            bestTrack = None
            nHitsBestTrack = -1
            
            for mcHTrack in trackToMcpTable.getAllTo(recoHMcp):
                goodHits = trackToGoodHits[mcHTrack]
                if goodHits > nHitsBestTrack:
                    nHitsBestTrack = goodHits
                    bestTrack = mcHTrack
                    
            isTrackBestTrack = 0 #False
            if bestTrack == track:
                isTrackBestTrack = 1 #True
                
            #Fill vectors for the track
            trackHelicalTrack = HelicalTrack(inputTrack=track, bField=bField) #computes the physical params and their errors from the reco data and vice-versa
            mcHelicalTrack = HelicalTrack(inputMcp=recoHMcp, bField=bField) #computes the physical params and their errors from the reco data and vice-versa
            bucketDict["track_nHits"][2][trackIndex] = len(track.getTrackerHits())
            bucketDict["track_nFalseHits"][2][trackIndex] = trackToFalseHits[hTrack]
            bucketDict["track_d0"][2][trackIndex] = trackHelicalTrack.d0
            bucketDict["track_z0"][2][trackIndex] = trackHelicalTrack.z0
            bucketDict["track_dca"][2][trackIndex] = trackHelicalTrack.dca
            bucketDict["track_px"][2][trackIndex] = trackHelicalTrack.p.X()
            bucketDict["track_py"][2][trackIndex] = trackHelicalTrack.p.Y()
            bucketDict["track_pz"][2][trackIndex] = trackHelicalTrack.p.Z()
            bucketDict["track_pt"][2][trackIndex] = trackHelicalTrack.p.XYvector().Mod()
            bucketDict["track_p"][2][trackIndex] = trackHelicalTrack.p.Mag()
            bucketDict["track_theta"][2][trackIndex] = trackHelicalTrack.p.Theta()
            bucketDict["track_theta_conv"][2][trackIndex] = convTheta(trackHelicalTrack.p.Theta())
            bucketDict["track_phi"][2][trackIndex] = trackHelicalTrack.phi 
            bucketDict["track_charge"][2][trackIndex] = trackHelicalTrack.charge
            bucketDict["track_sigma_d0"][2][trackIndex] = trackHelicalTrack.errorD0
            bucketDict["track_sigma_z0"][2][trackIndex] = trackHelicalTrack.errorZ0
            bucketDict["track_sigma_dca"][2][trackIndex] = trackHelicalTrack.errorDca
            bucketDict["track_sigma_px"][2][trackIndex] = trackHelicalTrack.errorPx
            bucketDict["track_sigma_py"][2][trackIndex] = trackHelicalTrack.errorPy
            bucketDict["track_sigma_pz"][2][trackIndex] = trackHelicalTrack.errorPz
            bucketDict["track_sigma_pt"][2][trackIndex] = trackHelicalTrack.errorPt
            bucketDict["track_sigma_p"][2][trackIndex] = trackHelicalTrack.errorP
            bucketDict["track_sigma_theta"][2][trackIndex] = trackHelicalTrack.errorTheta
            bucketDict["track_sigma_theta_conv"][2][trackIndex] = trackHelicalTrack.errorTheta
            bucketDict["track_sigma_phi"][2][trackIndex] = trackHelicalTrack.errorPhi
            
            bucketDict["track_mc_nHits"][2][trackIndex] = len(hitToMcpTable.allTo(recoHMcp))
            bucketDict["track_mc_d0"][2][trackIndex] = mcHelicalTrack.d0
            bucketDict["track_mc_z0"][2][trackIndex] = mcHelicalTrack.z0
            bucketDict["track_mc_dca"][2][trackIndex] = mcHelicalTrack.dca
            bucketDict["track_mc_x"][2][trackIndex] = mcHelicalTrack.origin.X()
            bucketDict["track_mc_y"][2][trackIndex] = mcHelicalTrack.origin.Y()
            bucketDict["track_mc_z"][2][trackIndex] = mcHelicalTrack.origin.Z()
            bucketDict["track_mc_d_origin"][2][trackIndex] = mcHelicalTrack.origin.Mag()
            bucketDict["track_mc_px"][2][trackIndex] = mcHelicalTrack.p.X()
            bucketDict["track_mc_py"][2][trackIndex] = mcHelicalTrack.p.Y()
            bucketDict["track_mc_pz"][2][trackIndex] = mcHelicalTrack.p.Z()
            bucketDict["track_mc_pt"][2][trackIndex] = mcHelicalTrack.p.XYvector().Mod()
            bucketDict["track_mc_p"][2][trackIndex] = mcHelicalTrack.p.Mag()
            bucketDict["track_mc_theta"][2][trackIndex] = mcHelicalTrack.p.Theta()
            bucketDict["track_mc_theta_conv"][2][trackIndex] = convTheta(mcHelicalTrack.p.Theta)
            bucketDict["track_mc_phi"][2][trackIndex] = mcHelicalTrack.Phi
            bucketDict["track_mc_pathlength"][2][trackIndex] = sys.float_info.max #TODO fix
            bucketDict["track_mc_pathlength_los"][2][trackIndex] = sys.float_info.max #TODO fix
            bucketDict["track_mc_distance"][2][trackIndex] = mcDistance[recoHMcp]
            bucketDict["track_mc_charge"][2][trackIndex] = mcHelicalTrack.charge
            bucketDict["track_mc_pdgid"][2][trackIndex] = recoHMcp.getPDG()
            bucketDict["track_mc_signal"][2][trackIndex] = 1 #TODO fix
            bucketDict["track_mc_findable"][2][trackIndex] = 1 #TODO fix
            bucketDict["track_mc_besttrack"][2][trackIndex] = isTrackBestTrack

        for mcpIndex, mcp in enumerate(mcParticles):
            hmcp = HLcioObject(mcp)

            mcHelicalTrack = HelicalTrack(inputMcp=mcp, bField=bField)
            #Fill vectors for the mcp
            bucketDict["mc_x"][2][mcpIndex] = mcHelicalTrack.origin.X() 
            bucketDict["mc_y"][2][mcpIndex] = mcHelicalTrack.origin.Y()
            bucketDict["mc_z"][2][mcpIndex] = mcHelicalTrack.origin.Z()
            bucketDict["mc_d_origin"][2][mcpIndex] = mcHelicalTrack.origin.Mag()
                              
            bucketDict["mc_px"][2][mcpIndex] = mcHelicalTrack.p.X()
            bucketDict["mc_py"][2][mcpIndex] = mcHelicalTrack.p.Y()
            bucketDict["mc_pz"][2][mcpIndex] = mcHelicalTrack.p.Z()
            bucketDict["mc_pt"][2][mcpIndex] = mcHelicalTrack.p.XYvector().Mag()
            bucketDict["mc_p"][2][mcpIndex] =  mcHelicalTrack.p.Mag()
            
            bucketDict["mc_nHits"] = len(mcParticleToTrackerHitDict.get(hmcp, []))
            bucketDict["mc_distance"][2][mcpIndex] = mcDistance[hMcp]
            bucketDict["mc_charge"][2][mcpIndex] = mcp.getCharge()
            bucketDict["mc_pdgid"][2][mcpIndex] = mcp.getPDG()
            bucketDict["mc_signal"][2][mcpIndex] = 1 #TODO fix
            bucketDict["mc_status"][2][mcpIndex] = mcp.getGeneratorStatus()
            bucketDict["mc_findable"][2][mcpIndex] = 1 #TODO fix
            if hMcp in reconstructedMcps:
                bucketDict["mc_reconstructed"][2][mcpIndex] = 1
            else:
                bucketDict["mc_reconstructed"][2][mcpIndex] = 0

            bucketDict["mc_d0"][2][mcpIndex] = mcHelicalTrack.d0
            bucketDict["mc_z0"][2][mcpIndex] = mcHelicalTrack.z0
            bucketDict["mc_dca"][2][mcpIndex] = mcHelicalTrack.dca
            bucketDict["mc_theta"][2][mcpIndex] = mcHelicalTrack.theta
            bucketDict["mc_theta_conv"][2][mcpIndex] = convTheta(mcHelicalTrack.theta)
            bucketDict["mc_phi"][2][mcpIndex] = mcHelicalTrack.phi
            bucketDict["mc_pathlength"][2][mcpIndex] = sys.float_info.max
            bucketDict["mc_pathlength_los"][2][mcpIndex] = sys.float_info.max
            
        tree.Fill()

    """
    for i, event in enumerate(reader):
        chargedMcParticles = []
        for mcp in event.getCollection(MCParticleCollection):
            if isLongLivedAndCharged(mcp):
                chargedMcParticles.append(mcp)

        signalMcParticles = chargedMcParticles[:] #TOTO differentiate from background

        for mcp in chargedMcParticles:
            if mcp in signalMcParticles or len(signalMcParticles) == 0:
                mc_signal.append(1)
            else:
                if keepOnlySignalMcParticles:
                    continue
                mc_signal.append(0)

                
    
        print >> sys.stderr, i
        ntuple = ROOT.TNtuple("ntuple", "event ntuple {0}".format(i), "pdg:px:py:pz")
        if i > 9:
            break
        for mcp in event.getCollection("MCParticlesSkimmed"):
            p = mcp.getMomentum()
            ntuple.Fill(mcp.getPDG(),p[0], p[1], p[2])

        ntuple.Write()
    """
    f.Write()
    f.Close()

def main():
    for fileName in sys.argv[1:]:
        createRootFile(fileName, fileName.replace(".slcio", ".root"))


if __name__ == "__main__":
    main()

