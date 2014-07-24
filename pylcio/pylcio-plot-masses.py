#! /bin/env python

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from pylciohelperhunctions import *

import sys

import numpy as np
from matplotlib import pyplot as plt


def main():
    if len(sys.argv) != 2:
        print "Error: script requires a slcio file as input!"
        return -1
    
    print "Opening argv[1] = " + sys.argv[1]
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( sys.argv[1] )
    

    masses = [reconstructEventMass(event) for event in reader]
    hist, bins = np.histogram(masses, 5)

    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    plt.show()
            
        
    
    

if __name__ == "__main__":
    main()

    
