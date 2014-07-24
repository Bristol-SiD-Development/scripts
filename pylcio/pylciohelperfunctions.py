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
