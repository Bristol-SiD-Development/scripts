from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

import math

def sumVectors(v1, v2):
    return [x + y for x,y in zip(v1, v2)]

#note: fourMomentum is [m_x, m_y, m_z, E]
def extractFourMomentum(reconstructedParticle):
    fourMomentum = [0, 0, 0, 0]
    for i, momentum in enumerate(reconstructedParticle.getMomentum()): #this is needed because the vector isn't properly subscriptable!
        if i < 4:
            fourMomentum[i] = float(momentum) #I don't even know anymore
        else:
            break
    return fourMomentum

def fourVectorModulus(fourMomentum):
    return math.sqrt( math.pow(fourMomentum[3], 2) - normalVectorModulus(fourMomentum[0:3]))

def normalVectorModulus(vector):
    return math.sqrt( sum( map( lambda x: math.pow(x, 2), vector ) ) )

def reconstructEventFourMomentum(event):
    jets = event.getCollection("RefinedJets")
    if len(jets) != 2:
        print "Error more than 2 jets in collection: found ({0})".format(len(jets))
        return -1

    jet_momenta =[extractFourMomentum(jet) for jet in jets]
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

    threeMomentumModulus = normalVectorModulus(threeMomentum)

    zUnitVector = [0, 0, 1]

    cos_theta = vectorDotProduct(threeMomentum, zUnitVector)/threeMomentumModulus
    theta = math.cos(cos_theta)
    return theta

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

def decaysToQQBar(root):
    daughters = root.getDaughters()

    qPDGs = range(1, 7)
    qBarPDGs = range(-6, 0)

    qs = filter(lambda p: any([p.getPDG() == qPDG for qPDG in qPDGs]),daughters)
    qBars = filter(lambda p: any([p.getPDG() == qPDG for qPDG in qBarPDGs]),daughters)

    for element in itertools.product(qs, qBars):
        if element[0].getPDG() == -element[1].getPDG():
            #print "found qqBar: {0} {1}".format(element[0].getPDG(), element[1].getPDG())
            return abs(element[0].getPDG())
    return None

def walkMcParticlesUntilQQBar(root, depth=0):
    qPDG = decaysToQQBar(root)
    if qPDG:
        return qPDG

    for daughter in root.getDaughters():
        ret = walkMcParticlesUntilQQBar(daughter, depth+1)
        if ret != -1:
            return ret
            
    return -1

def get_jet_flavor_from_mc(event):
    for mcParticle in event.getCollection("MCParticlesSkimmed"):
        if len(mcParticle.getParents()) == 0:
            return walkMcParticlesUntilQQBar(mcParticle, 0)
            break
