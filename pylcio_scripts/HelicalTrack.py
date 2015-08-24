from __future__ import division
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

import math as m
import numpy as np

import sys

import itertools

import ROOT

class HelicalTrack(object):
    #Becuse units are annoying
    fieldConversionFactor = 2.9979 * 10**(-4) 
    def __init__(self, inputMcp=None, inputTrack=None, bField=None):
        self.d0 = None
        self.z0 = None
        self.tanL = None
        self.omega = None
        self.phi = None
        self.dca = None
        self.p = None
        #self.mass = None
        self.origin = None
        self.charge = None
        #self.energy = None

        self.errorD0 = None
        self.errorPhi = None
        self.errorOmega = None
        self.errorZ0 = None
        self.errorTanL = None

        self.errorPt = None
        self.errorPx = None
        self.errorPy = None
        self.errorPz = None
        self.errorD0 = None
        self.errorZ0 = None
        self.errorTheta = None
        self.errorDca = None

        if bField != None:
            if inputMcp != None and inputTrack == None:
                self._init_from_mcp(inputMcp, bField)
            elif inputMcp == None and inputTrack != None:
                self._init_from_track(inputTrack, bField)
            elif inputMcp != None and inputTrack != None:
                raise Exception("Both inputMcp and inputTrack provided to HelicalTrack constructor. All params will be None.")
            else:
                raise Exception("Neither inputMcp nor inputTrack provided to HelicalTrack constructor.")
        else:
            raise Exception("bField not provided to HelicalTrack constructor.")

    def _init_from_mcp(self, mcParticle, bField):
        self.p = mcParticle.getMomentumVec()
        px, py, pz = self.p.X(), self.p.Y(), self.p.Z()
        #self.mass = mcParticle.getMass
        self.origin = mcParticle.getVertexVec()
        self.charge = mcParticle.getCharge()
        #self.energy = mcParticle.getEnergy()

        pt = m.sqrt(px*px + py*py)
        p = m.sqrt(pt*pt + pz*pz)
        
        cth = pz / float(p)
        self.Theta = m.acos(cth)

        #Calculate Radius of the Helix
        R = mcParticle.getCharge() * pt / (HelicalTrack.fieldConversionFactor * bField)
        
        #Slope in the Dz/Ds sense, tanL Calculation
        try:
            self.tanL = pz / float(pt)
        except ZeroDivisionError:
            self.tanL = sys.float_info.max
    
        self.phi = np.arctan2(py, px)
    
        mcOrigin = mcParticle.getVertexVec()
        mcCreationX, mcCreationY, mcCreationZ = mcOrigin.X(), mcOrigin.Y(), mcOrigin.Z()

        #Distance of closest approach Calculation
        xc = mcCreationX + R * np.sin(self.phi)
        yc = mcCreationY - R * np.cos(self.phi)

        Rc = m.sqrt(xc*xc + yc*yc)

        self.d0 = None
        if mcParticle.getCharge()>0:
            self.d0 = R - Rc
        else:
            self.d0 = R + Rc

        #azimuthal calculation of the momentum at the DCA, phi0, Calculation
        phi0 = np.arctan2(xc/(R-self.d0),  -yc/(R-self.d0))
        while phi0 < 0:
            phi0 += 2*m.pi
        while phi0 > 2*np.pi:
            phi0 -= 2*m.pi
           
        #z0 Calculation, z position of the particle at dca
        x0 = -self.d0 * np.sin(phi0)
        y0 = self.d0 * np.cos(phi0)
        arclength  = (((mcCreationX - x0) * np.cos(phi0)) + ((mcCreationY - y0)* np.sin(phi0)))
        self.z0 = mcCreationZ - arclength * self.tanL

        self.dca = np.sqrt(self.d0*self.d0 + self.z0*self.z0)
            
        self.omega = None
        try:
            self.omega = 1. / R
        except ZeroDivisionError:
            self.omega = 0

    def _init_from_track(self, track, bField):
        #Track params
        self.d0 = track.getD0()
        self.z0 = track.getZ0()
        self.tanL = track.getTanLambda()
        self.omega = track.getOmega()
        self.phi = track.getPhi()

        self.dca = np.sqrt(self.d0*self.d0 + self.z0*self.z0)

        #Track params errors (stored as lower triangular matrix in lcio)
        covariances = track.getCovMatrix()[0:15]
        self.errorD0 = np.sqrt(covariances[0])
        self.errorPhi = np.sqrt(covariances[2])
        self.errorOmega = np.sqrt(covariances[5])
        self.errorZ0 = np.sqrt(covariances[9])
        self.errorTanL = np.sqrt(covariances[14])        

        #Physical params
        pt = abs(HelicalTrack.fieldConversionFactor*bField / track.getOmega())
        px = pt * np.cos(self.phi)
        py = pt * np.sin(self.phi)
        pz = pt * self.tanL
        self.p = ROOT.TVector3(px, py, pz)

        referencePoint = track.getReferencePointVec()
        x = referencePoint.X() - self.d0 * np.sin(self.phi)
        y = referencePoint.Y() + self.d0 * np.cos(self.phi)
        z = referencePoint.Z() + self.z0
        
        
        self.origin = ROOT.TVector3(x, y, z)
        if self.omega > 0:
            self.charge = 1
        else:
            self.charge = -1
        
        # Physical params errors (see: https://svnweb.cern.ch/cern/wsvn/clicdet/trunk/analysis/src/contrib/cgrefe/tracking/TrackUncertainties.java)
        self.errorPt = self.errorOmega * bField * HelicalTrack.fieldConversionFactor / (self.omega**2)

        #Px and Py
        sigA2 = covariances[5] #omega, omega
        A = self.omega
        sigB2 = covariances[2] #PHI, PHI
        B = self.phi
        covAB = covariances[4] #OMEGA, PHI
        a = bField * HelicalTrack.fieldConversionFactor

        self.errorPx = np.sqrt(a*a/(A*A) * (np.power(np.cos(B)/A,2)*sigA2 + np.power(np.sin(B), 2)*sigB2 + 2*np.sin(B)*np.cos(B)/A*covAB))
        self.errorPy = np.sqrt(a*a/(A*A) * (np.power(np.sin(B)/A,2)*sigA2 + np.power(np.cos(B), 2)*sigB2 - 2*np.cos(B)*np.sin(B)/A*covAB))

        #Pz
        sigA2 = covariances[5] #OMEGA, OMEGA
        A = self.omega
        sigB2 = covariances[14] # TANLAMBDA, TANLAMBDA
        B = self.tanL
        covAB = covariances[12] #OMEGA, TANLAMBDA
        a = bField * HelicalTrack.fieldConversionFactor
        self.errorPz = np.sqrt(a*a/(A*A) * (B*B*sigA2/(A*A) + sigB2 - 2*B*covAB/A))
        
        #P
        sigA2 = covariances[5] #OMEGA, OMEGA
        A = self.omega
        sigB2 = covariances[14] #TANLAMBDA, TANLAMBDA
        B = self.tanL
        covAB = covariances[12] #OMEGA, TANLAMBDA
        a = bField * HelicalTrack.fieldConversionFactor
               
        self.errorP =  np.sqrt(a*a/(A*A) * ((1+B*B)*sigA2/(A*A) + B*B*sigB2/(1+B*B) - 2*B*covAB/(np.sqrt(1+B*B)*A)))

        #Theta
        sigA2 = covariances[14] #TANLAMBDA, TANLAMBDA
        A = self.tanL
        self.errorTheta =  np.sqrt(sigA2/np.power(A*A+1,2))
        

        #DCA
        sigA2 = covariances[0] #D0, D0
        A = self.d0
        A2 = A*A
        sigB2 = covariances[9] #Z0, Z0
        B = self.z0
        B2 = B*B
        covAB = covariances[6] #D0, Z0
               
        self.errorDca = np.sqrt(1/(A2+B2)*(A2*sigA2 + B2*sigB2 + 2*A*B*covAB))
