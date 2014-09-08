from __future__ import division
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

import math as m
import numpy as np

import sys

import itertools

import ROOT


#Have to use these as hashing Pylcio MCParticles doesn't seem to work...
class hashable_mc_particle(object):
    def __init__(self, mcParticle):
        self.momentum = mcParticle.getMomentum()[0], mcParticle.getMomentum()[1], mcParticle.getMomentum()[2]
        self.energy = mcParticle.getMomentum()[3]
        self.charge = mcParticle.getCharge()
        self.spin = mcParticle.getSpin()[0], mcParticle.getSpin()[1], mcParticle.getSpin()[2]
        self.time = mcParticle.getTime()
        self.vertex = mcParticle.getVertex()[0],mcParticle.getVertex()[1],mcParticle.getVertex()[2], 
        self.pdg = mcParticle.getPDG()

    def __hash__(self):
        return hash((self.momentum, self.energy, self.charge, self.spin, self.time, self.vertex, self.pdg))

    def __eq__(self, other):
        if other == None:
            return False
        else:
            return ((self.momentum, self.energy, self.charge, self.spin, self.time, self.vertex, self.pdg) == (other.momentum, other.energy, other.charge, other.spin, other.time, other.vertex, other.pdg))

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def getTanLambda(self):
        pt = np.sqrt( self.momentum[0]**2 + self.momentum[1]**2)  
        return  self.momentum[2] / pt

    def getTheta(self):
        pt = np.sqrt(self.momentum[0]**2 + self.momentum[1]**2)

        return np.arctan2(pt, self.momentum[2])

#see note on hashable_mc_particle
class hashable_reco_track(object):
    def __init__(self, recoTrack):
        self.chi2 = recoTrack.getChi2()
        #self.covMatrix = [element for element in recoTrack.getCovMatrix()[0:15]]
        self.D0 = recoTrack.getD0()
        self.dEdx = recoTrack.getdEdx()
        self.dEdXError = recoTrack.getdEdxError()
        self.Ndf = recoTrack.getNdf()
        self.omega = recoTrack.getOmega()
        self.phi = recoTrack.getPhi()
        self.radiusInnerHit = recoTrack.getRadiusOfInnermostHit()
        self.refPoint = recoTrack.getReferencePoint()[0], recoTrack.getReferencePoint()[1], recoTrack.getReferencePoint()[2]
        self.tanLambda = recoTrack.getTanLambda()
        self.Z0 = recoTrack.getZ0()

        self.trackerHits = [hashable_tracker_hit(hit) for hit in  recoTrack.getTrackerHits()]

    def __hash__(self):
        return hash((self.chi2, self.D0, self.dEdx, self.dEdXError, self.omega, self.phi,self.refPoint, self.tanLambda, self.Z0))
    def __eq__(self, other):
        if other == None:
            return False
        else:
            return (self.chi2, self.D0, self.dEdx, self.dEdXError, self.omega, self.phi,self.refPoint, self.tanLambda, self.Z0) == \
                (other.chi2, other.D0, other.dEdx, other.dEdXError, other.omega, other.phi,other.refPoint, other.tanLambda, other.Z0)
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def getTheta(self):
        return np.arctan2(1,self.tanLambda)


class hashable_tracker_hit(object):
    def __init__(self, trackerHit):
        self.energyDep = trackerHit.getEDep()
        self.position = trackerHit.getPosition()[0], trackerHit.getPosition()[1], trackerHit.getPosition()[2]
        self.quality = trackerHit.getQuality()
        self.time = trackerHit.getTime()

    def __hash__(self):
        return hash((self.energyDep, self.position, self.quality, self.time))
    def __eq__(self, other):
        if other == None:
            return False
        else:
            return (self.energyDep, self.position, self.quality, self.time) == (other.energyDep, other.position, other.quality, other.time)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    

def sumVectors(v1, v2):
    return [x + y for x,y in zip(v1, v2)]

#note: fourMomentum is [m_x, m_y, m_z, E]
def getFourMomentum(reconstructedParticle):
    fourMomentum = [0, 0, 0, 0]
    for i, momentum in enumerate(reconstructedParticle.getMomentum()): #this is needed because the vector isn't properly subscriptable!
        if i < 4:
            fourMomentum[i] = float(momentum) #I don't even know anymore
        else:
            break
    return fourMomentum

def fourVectorModulus(fourMomentum):
    return math.sqrt( math.pow(fourMomentum[3], 2) - threeVectorModulus(fourMomentum[0:3]))

def threeVectorModulus(vector):
    return math.sqrt( sum( map( lambda x: math.pow(x, 2), vector ) ) )

def reconstructEventFourMomentum(event):
    jets = event.getCollection("RefinedJets")
    if len(jets) != 2:
        print "Error more than 2 jets in collection: found ({0})".format(len(jets))
        return -1

    jet_momenta =[getFourMomentum(jet) for jet in jets]
    total_event_momentum = sumVectors(jet_momenta[0], jet_momenta[1])
    return total_event_momentum

def reconstructEventMass(event):
    total_event_momentum = reconstructEventFourMomentum(event)
    return fourVectorModulus(total_event_momentum)

def vectorDotProduct(v1, v2):
    return sum(map(lambda x,y: x*y, v1,v2))

def reconstructEventTheta(event):
    fourMomentum = reconstructEventFourMomentum(event)
    threeMomentum = fourMomentum[:3]

    threeMomentumModulus = threeVectorModulus(threeMomentum)

    zUnitVector = [0, 0, 1]

    cos_theta = vectorDotProduct(threeMomentum, zUnitVector)/threeMomentumModulus
    theta = math.acos(cos_theta)
    return theta

def getParticleCosTheta(particle):
    fourMomentum = getFourMomentum(particle)
    threeMomentum = fourMomentum[:3]

    threeMomentumModulus = threeVectorModulus(threeMomentum)

    zUnitVector = [0, 0, 1]

    cos_theta = vectorDotProduct(threeMomentum, zUnitVector)/threeMomentumModulus
    #theta = math.acos(cos_theta)
    return cos_theta


def reconstructEventEta(event):
    return -math.log(math.tan( reconstructEventTheta(event) / 2.))
    

def get_b_and_c_likenesses(event):
    collection = event.getCollection("RefinedJets")
    
    pidh = UTIL.PIDHandler(collection)
    algo = pidh.getAlgorithmID( "lcfiplus" )
    ibtag = pidh.getParameterIndex(algo, "BTag")
    ictag = pidh.getParameterIndex(algo, "CTag")

    likenesses = []

    for jet in collection: #should be two of them...
        pid = pidh.getParticleID(jet, algo)
        likenesses.append({"BTag": pid.getParameters()[ibtag], "CTag": pid.getParameters()[ictag]})
        
    return likenesses


def getDecayPDG(root):
    daughters = root.getDaughters()

    #print >> sys.stderr, [d.getPDG() for d in daughters]
    if len(daughters) == 0:
        print >> sys.stderr, "Warning: {0} has no daughters :(".format(root.getPDG())
        return 0
    elif len(daughters) == 1:
        return decaysToPPBar(daughters[0])
    elif len(daughters) == 2 and (abs(daughters[0].getPDG()) == abs(daughters[1].getPDG())):
        return abs(daughters[0].getPDG())
    elif (len(daughters) == 3) and (root.getPDG() in [d.getPDG() for d in daughters]):
        #print >> sys.stderr, "Warning: decay {0} -> {1} {2} {3} seems unlikely. Filtering {0} from daughters.".format(root.getPDG(), 
        #                                                                                                              daughters[0].getPDG(), 
        #                                                                                                              daughters[1].getPDG(), 
        #                                                                                                              daughters[2].getPDG())
        daughters = filter(lambda p: p.getPDG() != root.getPDG(), daughters)
        if len(daughters) == 2 and (abs(daughters[0].getPDG()) == abs(daughters[1].getPDG())):
            return abs(daughters[0].getPDG())

    print >> sys.stderr, "Error: Weird  decay ({2} body) happened {0} -> {1}".format(root.getPDG(), " ".join([str(d.getPDG()) for d in daughters]), len(daughters))
    return 0

def get_decay_product_of_interesting_mcParticle(event, interesting=[23, 25]):
    found_interesting_particles = []
    for mcParticle in event.getCollection("MCParticlesSkimmed"):
        if mcParticle.getPDG() in interesting and not mcParticle in found_interesting_particles:
            found_interesting_particles.append(mcParticle)

    interesting_particle = None
    if len(found_interesting_particles) == 0:
        return None
    elif len(found_interesting_particles) == 1:
        interesting_particle = found_interesting_particles[0]
    else:
        interesting_particle = max(lambda p: p.getEnergy(), found_interesting_particles)[0]

    return getDecayPDG(interesting_particle)    

def getTrackParamsVariances(recoTrack):
    covariances = recoTrack.getCovMatrix()
    variances = [None]*5
    
    for i in range(0, 5):
        index = int(  ( i * (i+3) ) / 2)
        variances[i] = covariances[ index ]
    return variances

def isLongLivedAndCharged(mcParticle):
    pdg =  mcParticle.getPDG() 
    if  (mcParticle.getGeneratorStatus() == 1) and ((abs(pdg) == 11) or (abs(pdg) == 13) or (abs(pdg) == 321) or (abs(pdg) == 211) or (abs(pdg) == 2212)):
        return True
    else:
        return False


def get_track_transverse_momentum(track, BField):
    #Becuse units are annoying
    fieldConversionFactor = 2.9979 * 10**(-4) 
    return abs(fieldConversionFactor*BField / track.getOmega())

def getTrackParams(mcParticle, BField):
    """
    This function should only be called on an mcParticle. 
    It will return [D0, phi0, omega, Z0, tan(Lambda)] as described at
    http://www-flc.desy.de/lcnotes/notes/LC-DET-2006-004.pdf
    """
    px, py, pz = getFourMomentum(mcParticle)[0:3]
    
    pt = m.sqrt(px*px + py*py)
    p = m.sqrt(pt*pt + pz*pz)
        
    cth = pz / float(p)
    theta = m.acos(cth)
    
    #Becuse units are annoying
    fieldConversionFactor = 2.9979 * 10**(-4) 
    #Calculate Radius of the Helix
    R = mcParticle.getCharge() * pt / (fieldConversionFactor * BField)
        
    #Slope in the Dz/Ds sense, tanL Calculation

    tanL = pz / float(pt)
    
    mcphi = np.arctan2(py, px)
    
    mcCreationX, mcCreationY, mcCreationZ = mcParticle.getVertex()[0], mcParticle.getVertex()[1], mcParticle.getVertex()[2]

    #Distance of closest approach Calculation
    xc   = mcCreationX + R * np.sin(mcphi)
    yc   = mcCreationY - R * np.cos(mcphi)

    Rc = m.sqrt(xc*xc + yc*yc)

    mcdca = None
    if mcParticle.getCharge()>0:
        mcdca = R - Rc
    else:
        mcdca = R + Rc
    #else:
    #    raise Exception("I don't understand neutral particles!")

    #azimuthal calculation of the momentum at the DCA, phi0, Calculation
    mcphi0 = np.arctan2(xc/(R-mcdca),  -yc/(R-mcdca))
    while mcphi0 < 0:
        mcphi0 += 2*m.pi
    while mcphi0 > 2*np.pi:
        mcphi0 -= 2*m.pi
           
    #z0 Calculation, z position of the particle at dca
    x0 = -mcdca * np.sin(mcphi0)
    y0 = mcdca * np.cos(mcphi0)
    arclength  = (((mcCreationX - x0) * np.cos(mcphi0)) + ((mcCreationY - y0)* np.sin(mcphi0)))
    z0 = mcCreationZ - arclength * tanL

    omega = None
    try:
        omega = 1. / R
    except ZeroDivisionError:
        omega = 0

    return [mcdca, mcphi0, omega, z0, tanL]


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
                print >> sys.stderr, "Warning both inputMcp and inputTrack provided to HelicalTrack constructor. All params will be None."
            else:
                print >> sys.stderr, "Warning neither inputMcp nor inputTrack provided to HelicalTrack constructor. All params will be None."
        else:
            print >> sys.stderr, "Warning bField not provided to HelicalTrack constructor. All params will be None."

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
        self.tanL = pz / float(pt)
    
        self.phi = np.arctan2(py, px)
    
        mcCreationX, mcCreationY, mcCreationZ = mcParticle.getVertex()[0], mcParticle.getVertex()[1], mcParticle.getVertex()[2]

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
    
    """        
    def getD0(self):
        return self.D0
    def getZ0(self):
        return self.Z0
    def getPhi(self):
        return self.Phi
    def getTanL(self):
        return self.tanL
    def getOmega(self):
        return self.Omega
    def getTheta(self):
        return self.Theta
    def getThetaConv(self):
    return 90. - 180.*abs(theta/np.pi - 0.5)
    """
