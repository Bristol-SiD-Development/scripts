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