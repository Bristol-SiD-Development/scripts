The shell script is a simple (if ugly) script to automate the SiD Sim-Reco chain. Currently it requires all of the input files to be in specific hardcoded directories in my (/afs/cern.ch/user/o/oreardon/) afs home.

It is set up to run the chain with the pythiaZPolebbbar.stdhep (found here: ftp://ftp-lcd.slac.stanford.edu/lcd/ILC/ZPole/stdhep/pythia/) input file although it can be edited with a simple find and replace.

The file BB_sid_dbd_vertexing.xml must also be edited to reflect any changes in the input and output files marlin uses for the LCFIplus vertexing.

The script is based on the 'From Zero to SiD' guide found here: https://confluence.slac.stanford.edu/display/~stanitz/From+Zero+to+SiD+-+Running+Sim+Reco


The python version is a bit nicer as most things can be set from the command line. However your marlin flavortagging steering file must set the following parameters (example settings shown) as it seems impossible to change them more nicely  (except by generating the xml at runtime from python...):


```xml
	<parameter name="FlavorTag.WeightsDirectory" type="string" value="/afs/cern.ch/user/o/oreardon/public/ilc/data/weightFiles/qq91" />
	<parameter name="FlavorTag.WeightsPrefix" type="string" value="qq91_v02_p01" />
	<parameter name="FlavorTag.D0ProbFileName" type="string" value="/afs/cern.ch/user/o/oreardon/public/ilc/data/vtxprobFiles/d0prob_zpole.root"/>
	<parameter name="FlavorTag.Z0ProbFileName" type="string" value="/afs/cern.ch/user/o/oreardon/public/ilc/data/vtxprobFiles/z0prob_zpole.root"/>
```