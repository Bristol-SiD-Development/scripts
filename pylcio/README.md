Directory to put scripts based on the pylcio bindings

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

Because of the insanity of some of what the pyLCIO methods return they are wrapped up in utility functions given in pylciohelperfunctions module 

The scripts with names like pylcio-print-masses.py and do roughly what you'd expect

Note that when it starts up pylcio prints a message about loading root dictionaries to the stdout (not the stderr!) so anytime you pipe the stdout of a script that imports these modules you should do so through the tail command:

```bash
tail -n +2
```

Using tail like this will simply write it's stdin to it's stdout starting from the second line
