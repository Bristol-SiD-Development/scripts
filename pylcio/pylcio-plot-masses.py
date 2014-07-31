#! /bin/env python

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
    if len(sys.argv) != 2:
        print "Error: script requires a slcio file as input!"
        return -1
    
    print "Opening argv[1] = " + sys.argv[1]
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( sys.argv[1] )
    

    #masses = [reconstructEventMass(event) for event in reader]
    for event in reader:
        print reconstructEventMass(event)

    return 0
    lower_cut=70
    upper_cut = 110
    masses = filter(lambda x: (lower_cut < x < upper_cut), masses)

    hist, bins = np.histogram(masses,30)

    width = (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2.

    fig = plt.figure()

    xmin, xmax = xlim = 70,110
    ymin, ymax = ylim = float(min(hist)), float(max(hist))
    
    ax = fig.add_subplot(111, xlim=xlim,ylim=ylim, autoscale_on=False)

    plt.bar(center, hist, align='center', width=width)

    plt.grid() 

    #ax.set_aspect('auto')
    plt.show()
            

if __name__ == "__main__":
    main()

    
