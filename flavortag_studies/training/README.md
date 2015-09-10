##LCFIPlus Training

Please see [here](https://svnsrv.desy.de/viewvc/marlinreco/ILDConfig/trunk/LCFIPlusConfig/README?revision=4787&view=markup) and [here](https://svnsrv.desy.de/viewvc/marlinreco/ILDConfig/trunk/LCFIPlusConfig/steer/README?revision=5001&view=markup) for the only useful hints at training I could find!!!

LCFIPlus flavortagging requires both vtxprob files (.root files) and lcfiweights files which come in the form of 4 sets of files(c0, c1, c2, c3).
These are then used by the flavortag proccessor in LCFIPlus. Currently i can not get the full training chain working.

###Notes

Things i have found while exploring training of note...

1. Input files i have produced have nmuon and nelection as zero, TrainMVA complains about this.
2. The original vtxprob files for the ZPole as found on LCFIPlusconfig, have been produced with an older version of root. Therefore definitly need to use your own produced with either ilcsoft v01-17-07 or v01-17-08. If not you have to deal with the joys of segmentation violations.
3. TrainMVA also complains about some of the book options passed from the steeringFiles are outdated. 
4. Not much documentation of this, therefore, easy to mismatch versions of the software and steering files, which is most likely the source of issues.

###makeWeights.py (Currently not working)

Python script for producing lcfiweights files from three sample .slcio files for...

1. Z->bb
2. Z->cc
3. Z->qq (light)

###SteeringFiles

Various versions of the steering files used by makeWeights.py, used for testing!

###TrackProb.C

The macro/trackProb.c file found in LCFIPlus, used for production of vtxprob files via root. 

