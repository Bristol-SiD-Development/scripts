#! /bin/env python2
from __future__ import division
from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from HelicalTrack import HelicalTrack
from FastHashableObject import FastHashableHit, FastHashableMcp, FastHashableTrack
from TrackAnalysis import TrackAnalysis

from createRootNtuples import ManyToManyTable, ManyToOneTable, isLongLivedAndCharged, createHitToMcpTable, createTrackToMcpTable

import sys
import math
import numpy as np

import pickle

#from scipy.optimize import curve_fit

def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))


def main():
    lcioReader = IOIMPL.LCFactory.getInstance().createLCReader()
    
    num_theta_bins = 100

    theta_bins = np.linspace(0, np.pi, num_theta_bins)
    d0_resolution_data = [[] for _ in xrange(num_theta_bins)]

    outputFileName = sys.argv[1]
    for fileName in sys.argv[2:]:
        lcioReader.open(fileName)
        for i, event in enumerate(lcioReader):
            print >> sys.stderr, i
            #if i > 1000:
            #    break
            for trackMcTruthLink in event.getCollection("TrackMCTruthLink"):
                track = trackMcTruthLink.getFrom()
                mcParticle = trackMcTruthLink.getTo()
                mcHelicalTrack = HelicalTrack(inputMcp=mcParticle, bField=5.)

                index = np.digitize([mcParticle.getMomentumVec().Theta()], theta_bins)[0]

                d0_resolution_data[index].append( mcHelicalTrack.d0 - track.getD0()  )
            
        lcioReader.close()
                 
    theta_histogram_bins_list = []
    for  theta, d0_resolution_datum in zip(theta_bins, d0_resolution_data ):
        if len(d0_resolution_datum) > 30:
            hist, bins = np.histogram(d0_resolution_datum, 10)

            theta_histogram_bins_list.append((theta, hist, bins))

        """
        width = (bins[1] - bins[0])
        center = (bins[:-1] + bins[1:]) / 2.
        
        p0 = [1., 0., 1.]
        coeff, var_matrix = curve_fit(gauss, center, hist, p0=p0)

        print "Theta={0}: A={1} mu={2} sigma={3}".format(theta,*coeff)
        """

    pickle.dump(theta_histogram_bins_list, open( outputFileName, "wb" ))

if __name__ == "__main__":
    main()
