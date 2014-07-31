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
    if len(sys.argv) != 2:
        print "Error: script requires a slcio file as input!"
        return -1
    
    print "Opening argv[1] = " + sys.argv[1]
    reader = IOIMPL.LCFactory.getInstance().createLCReader()
    reader.open( sys.argv[1] )
    
    for event in reader:
        likenesses = get_b_and_c_likenesses(event)
        actual_flavour = get_decay_product_of_interesting_mcParticle(event)
        for  likeness_dict in likenesses:
            print  str(actual_flavour) + " " + " ".join([str(likeness_dict["BTag"]),str(likeness_dict["CTag"])])
                         
if __name__ == "__main__":
    main()
