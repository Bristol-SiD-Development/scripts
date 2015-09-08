##Flavortag Studies

Scripts for flavortagging and analysis of DST input .slcio files. As ILC-DIRAC is currently unable to do flavortagging due to the need for weights files in a directory which cannot be achived within the input sandbox. Flavortagging can be done either on soolin or lxplus. This requires lcfiweights and vtxprob files (see /training for further details), basic versions of which can be found [here](https://svnsrv.desy.de/viewvc/marlinreco/ILDConfig/trunk/LCFIPlusConfig/), the README's on this page are also very usefull, especially with regards to steering files and LCFIPlus processors. 

Once a DST has been run through LCFIPlus flavortagging, the collection 'RefinedJets' within the .slcio files contains the btag and ctag data. In order to access this data, pyLCIO is employed. The btag and ctag data requires the use of a PIDHandler to be used (therefore it is more complex to get hold of than most data in the .slcio file). pyLCIO_tag.py reads .slcio files and places their btag and ctag data into an ntuple of a specific structure, this can then be read by pyROOT_tag.py to produce various histograms/plots. 

###env.sh

Bash script to setup LCIO and ROOT on lxplus.

```
source env.sh
```

###flavortag.py

Script to run DST(.slcio) files through LCFIPlus flavortagging. Note the steeringFile.xml must be modified to point to the vtxprob and lcfiweights files to be used. The version of ilcsoft needs to be sourced (source init_ilcsoft.sh) before this will work as Marlin needs to load its ahred libraries. Usage...

```
python flavortag.py DST_input.slcio -s steeringFile(default=sid_dbd_flavortag.xml) -g gearFile.gear -o outputDir -m PathToMarlin
```

###pyLCIO_tag.py

Takes an input .slcio file or an input directory containing multiple .slcio files and produces an output .root file containing 5 ntuples one for each z->qq decay type, within which the btag and ctag data from the files is stored. 

Structure of .root file output...
- output.root
	+ d_tags
		+ btag
		+ ctag
	+ u_tags
		+ btag
		+ ctag
	+ s_tags
		+ btag
		+ ctag
	+ c_tags
		+ btag
		+ ctag
	+ b_tags
		+ btag
		+ ctag

Usage...

```
python pyLCIO_tag.py -f inputDirectory -f inputFile.slcio -o outputDirectory -n outputName.slcio
```

Note, you can not define both an input directory and an input file, use one or the other not both.

###pyROOT_tag.py

Reads the output.root file produced by pyLCIO_tag.py applies realistic branching ratio's and combines the light quark data sets. Provides the option to produce a veriety of plots (all optional)...

1. Basic frequency vs btag/ctag value histograms. (--hist)
2. Fake rate vs efficiency plots. (--back)
3. Purity vs efficiency plots. (--pur)

Usage...

```
python pyROOT_tag.py input.root -o outputDirectoryForPlots -n basenameForOutputPlots --hist --back --pur -bins numberOfBinsInPlots
```

###test.root

A test .root file!!!