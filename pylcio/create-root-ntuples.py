#! /bin/env python2
import ROOT

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from pylciohelperfunctions import HelicalTrack

from HLcioObject import HLcioObject

from array import array

import sys

import numpy as np

class ManyToManyTable(object):
    def __init__(self):
        self.toDict = {}
        self.fromDict = {}
        #self.relationList = []
    def addFrom(self, fromObject):
        if not fromObject in self.fromList:
            self.fromDict[fromObject] = []
    def addTo(self, toObject):
        if not toObject in self.toList:
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


def getBucketDict():
    bucketDict = {"event": ('I',  array('i', [0])),
                  "Ntracks": ('I', array('i', [0])),
                  "nMCPs": ('I', array('i', [0])),
                  "track_nHits":['int', 'track'],
                  "track_nFalseHits":['int','track'],
                  "track_d0":['double','track'],
                  "track_z0":['double','track'],
                  "track_dca":['double','track'],
                  "track_px":['double','track'],
                  "track_py":['double','track'],
                  "track_pz":['double','track'],
                  "track_pt":['double','track'],
                  "track_p":['double','track'],
                  "track_theta":['double','track'],
                  "track_theta_conv":['double','track'],
                  "track_phi":['double','track'],
                  "track_charge":['int','track'],
                  "track_sigma_d0":['double','track'],
                  "track_sigma_z0":['double','track'],
                  "track_sigma_dca":['double','track'],
                  "track_sigma_px":['double','track'],
                  "track_sigma_py":['double','track'],
                  "track_sigma_pz":['double','track'],
                  "track_sigma_pt":['double','track'],
                  "track_sigma_p":['double','track'],
                  "track_sigma_theta":['double','track'],
                  "track_sigma_theta_conv":['double','track'],
                  "track_sigma_phi":['double','track'],
                  "track_mc_nHits":['int','track'],
                  "track_mc_d0":['double','track'],
                  "track_mc_z0":['double','track'],
                  "track_mc_dca":['double','track'],
                  "track_mc_x":['double','track'],
                  "track_mc_y":['double','track'],
                  "track_mc_z":['double','track'],
                  "track_mc_d_origin":['double','track'],
                  "track_mc_px":['double','track'],
                  "track_mc_py":['double','track'],
                  "track_mc_pz":['double','track'],
                  "track_mc_pt":['double','track'],
                  "track_mc_p":['double','track'],
                  "track_mc_theta":['double','track'],
                  "track_mc_theta_conv":['double','track'],
                  "track_mc_phi":['double','track'],
                  "track_mc_pathlength":['double','track'],
                  "track_mc_pathlength_los":['double','track'],
                  "track_mc_distance":['double','track'],
                  "track_mc_charge":['double','track'],
                  "track_mc_pdgid":['int','track'],
                  "track_mc_signal":['int','track'],
                  "track_mc_status":['int','track'],
                  "track_mc_findable":['int','track'],
                  "track_mc_besttrack":['int','track'],
                  "mc_nHits":['int', "mcp"], #done
                  "mc_d0":['double', "mcp"], #done
                  "mc_z0":['double', "mcp"], #done
                  "mc_dca":['double', "mcp"], #done
                  "mc_x":['double', "mcp"], #done
                  "mc_y":['double', "mcp"], #done
                  "mc_z":['double', "mcp"], #done
                  "mc_d_origin":['double', "mcp"],
                  "mc_px":['double', "mcp"], #done
                  "mc_py":['double', "mcp"], #done
                  "mc_pz":['double', "mcp"], #done
                  "mc_pt":['double', "mcp"], #done
                  "mc_p":['double', "mcp"], #done
                  "mc_theta":['double', "mcp"], #done
                  "mc_theta_conv":['double', "mcp"], #done
                  "mc_phi":['double', "mcp"], #done
                  "mc_pathlength":['double', "mcp"],
                  "mc_pathlength_los":['double', "mcp"],
                  "mc_distance":['double', "mcp"],
                  "mc_charge":['double', "mcp"], #done
                  "mc_pdgid":['int', "mcp"], #done
                  "mc_signal":['int', "mcp"],
                  "mc_status":['int', "mcp"], #done
                  "mc_findable":['int', "mcp"],
                  "mc_reconstructed":['int', "mcp"]}
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
    implementedKeys = ["event", "Ntracks", "nMCPs", "mc_x", "mc_y", "mc_z", "mc_px", "mc_py", "mc_pz", "mc_pt", "mc_p", "mc_d0", "mc_z0","mc_dca", "mc_theta", "mc_phi"]
    for key in implementedKeys:
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

        for key in implementedKeys:
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

        #Create a dictionary relating mcParticles to the hits they've caused
        mcParticleToTrackerHitDict = {}
        for hitMcpRelation in hitMcpRelations:
            hit = HLcioObject(hitMcpRelation.getFrom())
            mcp = HLcioObject(hitMcpRelation.getTo())
            try:
                mcParticleToTrackerHitDict[mcp].append(hit)
            except KeyError:
                mcParticleToTrackerHitDict[mcp] = [hit]
            
        trackToMcpTable = ManyToManyTable()
        for trackMcpRelation in trackMcpRelations:
            trackToMcpTable.addRelation(trackMcpRelation.getFrom(), trackMcpRelation.getTo())

        for mcpIndex, mcp in enumerate(mcParticles):
            hmcp = HLcioObject(mcp)
            bucketDict["mc_x"][2][mcpIndex] = mcp.getVertex()[0]
            bucketDict["mc_y"][2][mcpIndex] = mcp.getVertex()[1]
            bucketDict["mc_z"][2][mcpIndex] = mcp.getVertex()[2]
                              
            bucketDict["mc_px"][2][mcpIndex] = mcp.getMomentum()[0]
            bucketDict["mc_py"][2][mcpIndex] = mcp.getMomentum()[1]
            bucketDict["mc_pz"][2][mcpIndex] = mcp.getMomentum()[2]
            bucketDict["mc_pt"][2][mcpIndex] = np.sqrt( mcp.getMomentum()[0]**2 + mcp.getMomentum()[1]**2)
            bucketDict["mc_p"][2][mcpIndex] = np.sqrt( mcp.getMomentum()[0]**2 + mcp.getMomentum()[1]**2 + mcp.getMomentum()[2]**2 )
            
            bucketDict["mc_nHits"] = len(mcParticleToTrackerHitDict.get(hmcp, []))
            bucketDict["charge"][2][mcpIndex] = mcp.getCharge()
            bucketDict["mc_pdgid"][2][mcpIndex] = mcp.getPDG()
            bucketDict["mc_status"][2][mcpIndex] = mcp.getGeneratorStatus()

            mcHelicalTrack = HelicalTrack(mcp, bField)
            
            bucketDict["mc_d0"][2][mcpIndex] = mcHelicalTrack.getD0()
            bucketDict["mc_z0"][2][mcpIndex] = mcHelicalTrack.getZ0()
            bucketDict["mc_dca"][2][mcpIndex] = np.sqrt(mcHelicalTrack.getD0()**2 + mcHelicalTrack.getZ0**2)
            bucketDict["mc_theta"][2][mcpIndex] = mcHelicalTrack.getTheta()
            bucketDict["mc_theta_conv"][2][mcpIndex] = mcHelicalTrack.getThetaConv()
            bucketDict["mc_phi"][2][mcpIndex] = mcHelicalTrack.getPhi()
            
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

