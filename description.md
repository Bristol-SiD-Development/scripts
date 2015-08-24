##ILC SiD, Simulation, Reconstruction and Plotting

WORK IN PROGRESS :)

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
This first stage of lcsim (a java based framework for event reconstruction and analysis) takes the output .slcio file produced by the previous SLIC(GEANT4) simulation step. It then runs the digitization and tracking of each event through the defined detector.

lcsim contains the detector descriptions that can be easily used, particularly in ILC-DIRAC as they can be simply named, i.e "sidloi3", rather than defining an alias and pointing to the relevant files.

lcsim works via calling a series of drivers defined in a .xml steering file. Each driver is called along with the variables associated with it, for example...

```
    <driver name="VertexDigi"
            type="org.lcsim.recon.tracking.digitization.sisim.config.PixelDigiSetupDriver">
      <subdetectorNames>SiVertexBarrel SiVertexEndcap SiTrackerForward</subdetectorNames>
      <rawHitsCollectionName>VXD_RawTrackerHits</rawHitsCollectionName>
      <trackerHitsCollectionName>VXD_TrackerHits</trackerHitsCollectionName>
      <maxClusterSize>10</maxClusterSize>
      <noiseIntercept>0.</noiseIntercept>
      <noiseSlope>0.</noiseSlope>
      <noiseThreshold>100.</noiseThreshold>
      <readoutNeighborThreshold>100.</readoutNeighborThreshold>
      <seedThreshold>100.</seedThreshold>
      <neighborThreshold>100.</neighborThreshold>
      <oneClusterErr>0.288675135</oneClusterErr>
      <twoClusterErr>0.2</twoClusterErr>
      <threeClusterErr>0.333333333</threeClusterErr>
      <fourClusterErr>0.5</fourClusterErr>
      <fiveClusterErr>1.0</fiveClusterErr>
    </driver>
```
This lcsim step also requires a tracking strategies .xml file. lcsim usage...

```
	java -jar path_to_lcsim_jar/lcsim.jar steeringFile.xml -DinputFile=outputFromSlic.slcio -DtrackingStrategies=trackingStrategies.xml -DoutputFile=lcsimOutput.slcio
```

####slicPandora

slicPandora runs the Pandora Particle Flow Algorithm and produces Particle Flow objects which appear as an extra collection in the LCIO files, "PandoraPFOCollection". slicPandora requires both a settings file (.xml format) and a specific form of the detector geometry (.xml format). The detector geometry is a simple version and can be produced from the compact.xml description using the GeomConverter. The settings file contains variables that determine how the algorithm is run. 

slicPandora requires shared libraries, therefore it is very key that you source "init_ilcsoft.sh" when attempting to use it, or go to its file within the directory and source "build_env.sh", however, this can sometimes not allow marlin to run in the following step when it attempts to load its shared libraries. 

slicPandora usage...

```
  path_to_slicPandora/PandoraFrontend -g pandoraGeometry.xml -c PandoraSettings.xml -i outputFromLcsim.slcio -o pandoraOutput.slcio
```

####Marlin (LCFIPlus vertexing)

Once the Particle Flow Algorithm has been run, LCFIPlus can use the "PandoraPFOCollection" to conduct vertex finding, jet finding and flavor tagging. Marlin takes a steering file (.xml format) which defines a series of processors and associated variables. The general layout is given by...

```
  <marlin>
  <execute>
    <processor name="myprocessor"/>
  </execute>
  <global>
    # Global Parameters
  </global>
  <processor name="myprocessor" type="LcfiplusProcessor">
    # Prosessor specific parameters
  </processor>
  </marlin>
```

Example steering files for all LCFIplus processes are availiable [here](https://svnsrv.desy.de/viewvc/marlinreco/ILDConfig/trunk/LCFIPlusConfig/steer/). I recommend reading the README as it explains how LCFIPlus can be used. A gear file (.gear, but same as .xml format) is also required, but a very simple version just containing magnetic field infomation can be linked to within the steering file. Initially Marlin is used to run the "PrimaryVertexFinder" and "BuildUpVertex" processors. The input and output files can either be defined in the steering file or can be defined when calling Marlin, usage...

```
  path_to_marlin/Marlin vertexing.xml --global.LCIOInputFiles=slicPandoraOutput.slcio --global.LCIOOutputProcessor.LCIOOutputFile=vertexingOutput.slcio
```

####lcsim (DST production)

The large .slcio file is then converted into DST format (still .slcio extension), which removes the majority of the no longer needed collections within the LCIO file. This employs lcsim again, with a deifferent steering file to call different drivers. Usage...

```
  java -jar path_to_lcsim_jar/lcsim.jar steeringFile.xml -DinputFile=outputFromVertexing.slcio -DrecFile=outputThatContainsAllCollections.slcio -DdstFile=DSTOutput.slcio
```

####Marlin (LCFIPlus flavortagging)

We can now run the flavortagging processors from LCFIPlus, "JetClustering", "JetVertexRefiner", "FlavorTag" and "ReadMVA". In addition to the steering file, weights files and vtxprobfiles are required by the flavortagging, these contain variables described [here](http://arxiv.org/pdf/1506.08371v1.pdf). These files depend on the energy of the beam used and the detector geometry (NEED TO WRITE SCRIPT TO MAKE THESE). The location of these files is defined in the steering.xml file. This stage adds the "RefinedJets" collection to the DST .slcio file produced in the previous stage, this contains the btag and ctag data for each jet (proves more difficult to get out of .slcio files than most things).

Marlin, LCFIPlus Flavortagging usage...

```
  path_to_marlin/Marlin flavortagging.xml --global.LCIOInputFiles=DST.slcio --global.LCIOOutputProcessor.LCIOOutputFile=flavortagOutput.slcio
```

###Versions, locations, enviroment variables

####v01-17-05

####v01-17-07

###Required Files summary

*SLIC Geometry
*lcsim Geometry
*Pandora Geometry
*lcsim pre pandora steering
*lcsim tracking strategies
*pandora settings
*LCFIPlus vertexing steering
*Gear file
*lcsim post pandora(DST creation) steering
*LCFIPlus flavortagging steering

###ILC-DIRAC

###LCIO

####Data Structure

####API

###pyROOT/pyLCIO