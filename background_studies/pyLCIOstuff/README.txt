firstly install root with lcio and python enabled - this web page is helpful:

https://confluence.slac.stanford.edu/display/hpsg/Loading+LCIO+Files+into+ROOT

To run pyLCIO with root you need to set the environment first. Type source mysetup.sh to set them - you will need to edit the mysetup file in an editor (I use sublime text). 
	-edit path to root folder
	-your lcio trunk folder

Put your .slcio files in the same folder as the .py file you're running - or you can define the directory.

In terminal type "python pythonscript.py -f thefile.sclio" to run with a specific file

BeamCalhist-z.py:	Makes a 2D histogram of the hits on the negative Z end of the 						beam calorimeter.

BeamCalhist.py:		Makes 2D histogram of the hits of the beam calorimeter.

BeamCalhist+z.py:	Makes a 2D histogram of the hits on the positive Z end of the 						beam calorimeter.

hitCounts.py:		Makes a histogram of hits per each sub-detector.

momHist.py:			Makes a histogram of the tansverse mmenta of the e+ and e-.

pCounts.py:			Makes a histogram of the number of each particle type.

posPlotBcal.py:		Plots x y z scatter of hits on the beam calorimeter.

posPlotPart:		Plots x y z scatter of starting positions of interesting 							particles.

pyLCIO_e.py:		Just looked at the properties of the electrons before they were 					ran through slic.

Tmoms.py:			Plots a histogram of transverse momenta of particles that left 						the detector.

zangle.py:			Plots the zenith angle of the electrons and positrons. Includes 					a cut for particluar transverse momentum.