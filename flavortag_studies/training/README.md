##LCFIPlus Training

Please see [here](https://svnsrv.desy.de/viewvc/marlinreco/ILDConfig/trunk/LCFIPlusConfig/README?revision=4787&view=markup) and [here](https://svnsrv.desy.de/viewvc/marlinreco/ILDConfig/trunk/LCFIPlusConfig/steer/README?revision=5001&view=markup) for the only useful hints at training I could find!!!

###lcfiweights

Can produce .root training files to then be used by TMVA in the trainMVA LCFIPlus processor, these appear to contain the appropriate data. However...

TMVA keeps crashing when producing the c2 round of weights...

###vtxprob files

Currently been unable to do, appears to run fine, but produces no output...

###makeWeights.py

Python script for producing lcfiweights files from three sample .slcio files for...

1. Z->bb
2. Z->cc
3. Z->qq (light)

###SteeringFiles

Various versions of the steering files used by makeWeights.py, used for testing!

###trackProb.py

Python version of the macro/trackProb.c file found in LCFIPlus, used for production of vtxprob files.

