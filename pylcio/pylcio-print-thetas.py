#! /bin/env python2
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from pylciohelperfunctions import *

import sys

import numpy as np
import matplotlib.colors as col
from matplotlib import pyplot as plt
from matplotlib.pyplot import cm

def main():
    tag = None
    if len(sys.argv) < 2:
        print "Error: script requires a slcio file as input!"
        return -1
    #if len(sys.argv) == 3:
    #    tag = sys.argv[2]
    
    for f in sys.argv[1:]:
        reader = IOIMPL.LCFactory.getInstance().createLCReader()
        reader.open(f)
    
        for event in reader:
            actual_flavour = None
            if tag:
                actual_flavour = tag
            else:
                actual_flavour = get_decay_product_of_interesting_mcParticle(event)
    
            for jet in event.getCollection("RefinedJets"):
                print "{0} {1}".format(actual_flavour, getParticleCosTheta(jet))
        reader.close()
if __name__ == "__main__":
    main()
