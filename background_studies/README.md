###Simulation of pairs.dat files in SLIC

All is based on the page [here](https://wikis.bris.ac.uk/display/sid/Simulation+of+the+background+events+for+the+SiD+detector)

####What you need

1. GuineaPig Converter, with all the .jar files in the /lib folder.
2. Access to a slic version (/cvmfs or /afs).
3. lcsim-bin.jar to merge events.

####pairsSimulation.py

This script run the simulation chain for pairs.dat files for me. Some of the paths will need changing in order for it to be used again. Aswell as your own versions of the GuineaPig Converter ([here](https://github.com/Schuea/GuineaPigConverter/tree/master/GuineaPig_conversion)) and an lcsim-bin.jar (can get from [here](http://srs.slac.stanford.edu/nexus/index.html#nexus-search;quick~lcsim distribution)). Note that you need to source "init_ilcsoft.sh" for whichever version of ilcsoft including slic you are using.

Note that the simulation of the events takes a while. For a file of ~200K MCparticles from a pairs.dat file, this will take a few hours. Therefore moving this to the grid would help!

####merge.xml

Used as the steering file for the lcsim merging step, within "pairsSimulation.py". The input and output files are defined so it works with the script which then deletes all intemediate files to just leave the final output.slcio file. 