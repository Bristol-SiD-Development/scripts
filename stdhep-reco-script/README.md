This is a simple (ugly) script to automate the SiD reco chain. Currently it requires all of the input files to be in spesific hardcoded directories in my (/afs/cern.ch/user/o/oreardon/) afs home.

It is set up to run the chain with the pythiaZPolebbbar.stdhep (found here: ftp://ftp-lcd.slac.stanford.edu/lcd/ILC/ZPole/stdhep/pythia/) input file although can be edited to change this with a simple find and replace.

The file BB_sid_dbd_vertexing.xml must also be edited to reflect any changes in the files marlin should input and output for the LCFIplus vertexing.

The script is heavily (entirely) based on the from zero to SiD guide found here: https://confluence.slac.stanford.edu/display/~stanitz/From+Zero+to+SiD+-+Running+Sim+Reco