#Overall
To run either script you must have access to afs as they depend heavily on things in /afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05/ and lightly on files in my public directory (for flavortagging).

Both scripts are heavily based on the 'From Zero to SiD' guide found [here](https://confluence.slac.stanford.edu/display/~stanitz/From+Zero+to+SiD+-+Running+Sim+Reco) some things  must be changed in the sample xml files provided [here](https://svnsrv.desy.de/viewvc/marlinreco/ILDConfig/trunk/LCFIPlusConfig/steer/) to make them compatable with the sidloi3 detector files. 

##Notes on org.lcsim:
###Dodgy workaround
1. Rather than having it passed on the command line org.lcsim takes it's detector geometry from a database described [here](https://confluence.slac.stanford.edu/display/ilc/Conditions+Database+Overview)
2. If you are making significant changes to the detector you therefore need to point org.lcsim at the new version as described [here](https://confluence.slac.stanford.edu/display/ilc/Creating+a+New+Detector+Description)
3. A sample ~/.lcsim/alias.properties is below
4. The directory pointed to by the alias should (at a minimum) contain a compact.xml and a detector.properties file

####Sample alias.properties:
```
mySidLoi3: file:///afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/sidloi3_edited

```

###Solution to org.lcsim crashing when given a detector with name != "sidloi3"
Not having the "TrackSubdetectorHitNumbers" driver in the lcsim_prepandora steering file is the correct solution to this problem as it is the only one which requires the detector name "sidloi3". It requires this because its method for working out in what subdetector is totally dependent on the detector geometry being exactly that of sidloi3. Furthermore the data it writes to the .slcio file seems to not be used at all.

Having done this give your detector a new name!

##Changes in marlin flavortag steering file:
1. The parameter "PFOCollection" should have value "PandoraPFOCollection" instead of "PandoraPFOs"
2. The parameter "TrackHitOrdering" should have value "0" instead of "1"
3. The parameter "ReadSubdetectorEnergies" should have value "0" instead of "1" (this avoids a seg fault on line 424 of the LCIOStorer.cc source file)
4. The parameter "TrackMinTPCHits" should have value "0" (this avoids a seg fault)
5. The following parameters should be changed to they point to the correct directory (ie change the paths to where you cloned this repo). I would have had the script do this automagically but apparently you can't override parameters if they have more than one full stop in them from the command line
   * FlavorTag.WeightsDirectory
   * FlavorTag.D0ProbFileName
   * FlavorTag.Z0ProbFileName
    

Also note that the gear.xml file that is passed to marlin flavortag is a dummy containing only magnetic field information.

#Shell script

The shell script is a simple (if ugly) script to automate the SiD Sim-Reco chain. Currently it requires all of the input files to be in specific hardcoded directories in my (/afs/cern.ch/user/o/oreardon/) afs home.

It is set up to run the chain with the pythiaZPoleccbar-0-1000.stdhep (found [here](ftp://ftp-lcd.slac.stanford.edu/lcd/ILC/ZPole/stdhep/pythia/)) input file although it can be edited with a simple find and replace.

The file BB_sid_dbd_vertexing.xml must also be edited to reflect any changes in the input and output files marlin uses for the LCFIplus vertexing.

#Python script

The python version is a bit nicer as most things can be set from the command line. However your marlin flavortagging steering file must set the following parameters (example settings shown) as it seems impossible to change them more nicely  (except by generating the xml at runtime from python...). This is because the overloading of parameters from the command line chokes on parameters with more than one '.' in them:


```xml
	<parameter name="FlavorTag.WeightsDirectory" type="string" value="/afs/cern.ch/user/o/oreardon/public/ilc/data/weightFiles/qq91" />
	<parameter name="FlavorTag.WeightsPrefix" type="string" value="qq91_v02_p01" />
	<parameter name="FlavorTag.D0ProbFileName" type="string" value="/afs/cern.ch/user/o/oreardon/public/ilc/data/vtxprobFiles/d0prob_zpole.root"/>
	<parameter name="FlavorTag.Z0ProbFileName" type="string" value="/afs/cern.ch/user/o/oreardon/public/ilc/data/vtxprobFiles/z0prob_zpole.root"/>
```
