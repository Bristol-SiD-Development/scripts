###Simulation of pairs.dat files in SLIC

All is based on the page [here](https://wikis.bris.ac.uk/display/sid/Simulation+of+the+background+events+for+the+SiD+detector)

What you need...
	-GuineaPig Converter, with all the .jar files in the /lib folder.
	-Access to a slic version (/cvmfs or /afs).
	-lcsim-bin.jar to merge events.

####pairsSimulation.py

This script run the simulation chain for pairs.dat files for me. Some of the paths will need changing in order for it to be used again. Aswell as your own versions of the GuineaPig Converter and an lcsim-bin.jar. Note that you need to source "init_ilcsoft.sh" for whichever version of slic you are using for it to work.

####merge.xml

Used as the steering file for the lcsim merging step, within "pairsSimulation.py". The input and output files are defined so it works with the script which then deletes all intemediate files to just leave the final output.slcio file. 