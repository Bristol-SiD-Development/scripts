Directory to put scripts based on the pylcio bindings

#Prerequisites
In order to use pylcio you should add the flollowing to your ~/.bashrc (note that the paths are subject to change)

```bash
# ~/.bashrc 
#-------------------------------------------------------------
# Environment variables to enable the lcsoft pyroot interpreter
#-------------------------------------------------------------
export ILCSOFT_PATH=/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05
export ROOTSYS=$ILCSOFT_PATH/root/5.34.10
export PYTHONDIR=/usr/lib/python2.6/site-packages
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH

#-----------------------------------------------------
# Environment variables to enable the pylcio module(s)
#-----------------------------------------------------
export LCIO=$ILCSOFT_PATH/lcio/v02-04-03
export PYTHONPATH=$LCIO/src/python:$PYTHONPATH
```

#Disclaimer
I do not claim these do anything useful.If they trash your data, explode your computer or eat your cat you're on your own.

#General info
##Annoying messages on stdout
Note that when you import a  pylcio module it prints a message about loading root dictionaries to the stdout (not the stderr!) so anytime you pipe the stdout of a script that imports these modules you should do so through the tail command:

```bash
tail -n +2
```

Using tail like this will simply write it's stdin to it's stdout starting from the second line

Alternatively you can do dodgy things like redefine sys.stdout to be a file pointing at /dev/null in a block around the imports but its probably simpler to use tail.

##Hashing LCIO objects

Currently it is (I think) impossible to use the pylcio classes in hashmap (or dictionary) structures. I wrote up some wrapper classes in FastHashableObjects.py. If you subclass FastHashableObject for your class you should end up with a thin wrapper class which can be hashed as expected.
##ROOT TTree output

See createRootNtuples to get an idea of how *ugly* it is working with root TTrees in python. To put primitive python types (int, float etc.) in the TTree you (apparently) need to use the array module to simulate c style (unchecked) pointers. This neatly gets around all of the safety of working in python. If you do the wrong things then the python interpreter will seg-fault. Usually it does this some way from where the error occoured (often when you call TTree.Fill() or TBranch.Fill()). 

The createRootNtuples module is currently not hugely useful but if the pathlength parameters are implemented (see here for an example http://svn.cern.ch/reps/clicdet/trunk/analysis/src/contrib/cgrefe/tracking/TrackingEfficiency.java) then it could be used in conjunction with Christain Greffe's plotting code to do tracking studies.  

# My scripts
## General pattern
Most of my scripts take one or more lcio filenames and iterate over them printing out information to stdout (remember to pipe it through tail). For example pylcioPrintBCLikenesses.py iterates over the input files and for each one loops over every event. For every event it attempts to find a Z->qq event and it prints out the theta angle, the actual (MC) PID and the b and c likeness of each one.

Most were never intended to be public so ignore (or fix :)) any bad practice. Pull requests are always welcome! A good start would probably be to replace the rampant abuse of sys.argv with the argparse module

## Specific Scripts

### createRootNtuples

An attempt to mimic the org.lcsim driver [here](https://svnweb.cern.ch/cern/wsvn/clicdet/trunk/analysis/src/contrib/cgrefe/tracking/TrackingEfficiency.java) as it requires unsupported software (ROOTWrapperJNI). Unfortunately this was only partially successful as a fair amount of work would be required porting the "swimmer" infrastructure to python so that the path lengths could be written correctly.

It currently processes a z->qq event in about 0.25 of a second running interactively on an LXPlus node.

### pylcioPrintBCLikenesses.py

Loops over all arguments assuming they're filenames for lcio files. Loops over each event and prints out the following string for the two main jets (if it finds them). This is useful for doing flavour tagging studies after lcfiPlus has processed your data.

theta true_flavour b_likeness c_likeness

Bad things will happen unless there exists a z->qq or h->qq decay or if the MC data isn't in a format I've anticipated (often the mother -> daughter information is not correct). It definately works on the pythia ZPole->uu, dd, ss, cc, bb samples found [here](ftp://ftp-lcd.slac.stanford.edu/lcd/ILC/ZPole/stdhep/pythia/) though.

### pylcioPrintHitsPerTrackTheta.py

Simple script that loops over every track in every event in every file and prints out it's theta and the number of hits associated with it

### pylcioPrintTrackEfficienciesPuritiesPt.py

Uses an outdated defintion of a good and fake track and is generally a bit dodgy. Probably don't use!

### pylcioPrintTrackEfficienciesPuritiesTheta.py

Used to generate the track efficiency and purity plots given in my presentation [here](https://agenda.linearcollider.org/conferenceDisplay.py?confId=6516). Needs updating to use the relational table classes (currently just uses *loads* of dicts).

The first argument should be the first event number to be processed in each file the second the last event number and all further arguments should be input file names (it writes it's output to sys.stdout).

### pylcioPrintTrackParamResolutionTheta.py

Used to generate the d0 resolution plot given in my presentation [here](https://agenda.linearcollider.org/conferenceDisplay.py?confId=6516). Needs rewriting as usage currently involves commenting out and uncommenting bits of main.

It has two modes of operation (curently controlled by commenting) either it reads in slcio files and outputs pickled data for the second stage or it reads in picked data from the first stage, and creates a histogram for each theta bin.This is becase the first stage takes a long time to run and the second required some tweaking.

### pylcioPrintTrackParams.py

Prints out track paramters, their variances and true (MC) values for every track which has been related to a mc particle with an LCRelation. Useful if you want to create pull diagrams for this data.

### pylcioTest.py

Horrendous mess of scratch space used to test various ideas about how pylcio worked. Probably don't even look at this one...

### pylciohelperfunctions.py

A horrendous mess of many unrelated functions and classes. 
