This is a simple (if ugly) script to automate the SiD Sim-Reco chain. Currently it requires all of the input files to be in specific hardcoded directories in my (/afs/cern.ch/user/o/oreardon/) afs home.

It is set up to run the chain with the pythiaZPolebbbar.stdhep (found here: ftp://ftp-lcd.slac.stanford.edu/lcd/ILC/ZPole/stdhep/pythia/) input file although it can be edited with a simple find and replace.

The file BB_sid_dbd_vertexing.xml must also be edited to reflect any changes in the input and output files marlin uses for the LCFIplus vertexing.

The script is based on the 'From Zero to SiD' guide found here: https://confluence.slac.stanford.edu/display/~stanitz/From+Zero+to+SiD+-+Running+Sim+Reco
