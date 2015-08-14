##ILC SiD, Simulation, Reconstruction and Plotting

WORK IN PROGRESS :(

###The SIM/RECO chain

####SLIC
SLIC takes an input .stdhep file, this contains a number of events to run through the simulation. The nature of these events are usually known, with all events in an .stdhep file being Z->bbar for example. A good source of .stdhep input files is the SLAC mass storage server described [here](https://confluence.slac.stanford.edu/display/ilc/Standard+Model+Data+Samples). You can browse all the files at, ftp://ftp-lcd.slac.stanford.edu/lcd/ILC.

SLIC also requires a detector geometry description in the .lcdd format, this is a detailed description and can be generated from the simple compact.xml format using geomConverter, scripts for which are in the geomConverter folder. All detector descriptions that can be used simply (without setting up an alias) can be found on the lcsim detector page [here](http://www.lcsim.org/detectors/).

SLIC can take in a macro file, this can contain paths to the various inputs, but these can also be passed as arguments when calling SLIC. A full list of the SLIC command line arguments and macro commands is given [here](https://twiki.cern.ch/twiki/bin/view/CLIC/SLIC). A macro can be as simple as...

```
	/physics/select QGSP_BERT
	/run/initialize
```

SLIC usage...

```
	path_to_slic/SLIC.sh -g geometry.lcdd -i input.stdhep -o outputfile.slcio -r numberOfEvents -m macroFile.mac
```

SLIC outputs a .slcio file. This is an LCIO file used by all the different stages of the SIM/RECO.

####lcsim (digitization and tracking)

####slicPandora

####Marlin (LCFIPlus vertexing)

####lcsim (DST production)

####Marlin (LCFIPlus flavortagging)

###Versions, locations, enviroment variables

###Required Files summary

###ILC-DIRAC

###LCIO

####Data Structure

####API

###pyROOT/pyLCIO