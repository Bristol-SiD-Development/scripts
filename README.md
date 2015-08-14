scripts
=======

Scripts for running the SiD software chain and for pulling data out of the resulting slcio files.

Documentation in process of being improved...

If necessary please email jt12194@my.bristol.ac.uk or or1426@my.bristol.ac.uk(no longer working on project)

I recommend you read description.md for full overview of the ILC SiD SIM/RECO chain.

###GeomConverter
Contains scripts to convert compact geometry descriptions (.xml) into the other forms...
- .lcdd, detailed and large detector description used by SLIC (GEANT4).
- pandora.xml, small description used by slicPandora in the particle flow analysis.
- .heprep, not used in the sim/reco chain but can be produced anyway.

###ILC-DIRAC
Contains everything needed to run the SIM/RECO chain on ILC-DIRAC...
- Descriptions of how to obtain certificates and setup the ILC-DIRAC enviroment.
- Scripts to submit jobs to ILC-DIRAC
- Steering files required by ILC-DIRAC to run various stages of the SIM/RECO.

Currently the flavortaging step is not included in the main chain as this requires weights files whose location is specified within the steering.xml file. Can't get this to work with ILC-DIRAC but shall look for solution to incorporate this stage.

###lcsimDrivers
Test lcsim driver along with build instructions and samle steering file.

###Parallel-reco-jobs
A script to run the stdhep-reco-chain in multiple LXBatch jobs, unnecessary if ILC-DIRAC can be used.

###pylcio
Scripts to pull the data from the resulting .slcio files at the end of the SIM/RECO, a bit messy, requires reorganisation, and detailed documentation on how ROOT/pyROOT/LCIO/pyLCIO work etc...

###stdhep-reco-script
The simple stdhep-reco-chain, calls each of the seperate parts of the chain from a python script, unnecessary if ILC-DIRAC can be used.

1. SLIC, to run the simulation in GEANT4.
2. lcsim to run the digitzation and the tracking.
3. SlicPandora to do the ParticleFlowAnalysis.
4. LCFIPlus to do the Vertexing.
5. lcsim to produce DST's
6. LCFIPlus to do the flavortaging.

###root-lcio-setup-script.sh
script to setup the enviroment variables in order to use pyROOT with LCIO, not the paths may need updating.
