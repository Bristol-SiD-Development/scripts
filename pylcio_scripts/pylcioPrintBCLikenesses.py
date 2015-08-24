#! /bin/env python2
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from pylciohelperfunctions import *

import sys
import numpy as np

def main():
    tag = None
    if len(sys.argv) < 2:
        print "Error: script requires a slcio file as input!"
        return -1
    #if len(sys.argv) == 3:
    #    tag = sys.argv[2]
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    for f in sys.argv[1:]:

        reader.open( f)
    
        for i, event in enumerate(reader):
            
            try:
                likenesses = get_b_and_c_likenesses(event)
                actual_flavour = None
                if tag:
                    actual_flavour = tag
                else:
                    actual_flavour = get_decay_product_of_interesting_mcParticle(event)
                for jet, likeness_dict in zip(event.getCollection("RefinedJets"), likenesses):
                
                    momentum = jet.getMomentumVec()
            
                    theta = momentum.Theta()

                    print str(theta) + " " + str(actual_flavour) + " " + " ".join([str(likeness_dict["BTag"]), str(likeness_dict["CTag"])])
            except:
                print >> sys.stderr, "Wat"
        reader.close()
if __name__ == "__main__":
    main()
