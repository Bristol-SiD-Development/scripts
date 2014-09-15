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

~~Because of the insanity of some of what the pyLCIO methods return they are wrapped up in utility functions given in pylciohelperfunctions module~~

The helper functions are actually less useful. There exist methods which sort out most of the bad behavior in pylcio but many of them are poorly (or just not) documented.

For example everywhere where there is a method returning a length 3 array a decorator method exists returning a ROOT TVector3.

Note that when it starts up pylcio prints a message about loading root dictionaries to the stdout (not the stderr!) so anytime you pipe the stdout of a script that imports these modules you should do so through the tail command:

```bash
tail -n +2
```

Using tail like this will simply write it's stdin to it's stdout starting from the second line

Currently it is impossible to use the pylcio classes in hashmap (or dictionary) structures. I wrote up some wrapper classes in FastHashableObjects.py. If yo subclass FastHashableObject for your class you should end up with a thin wrapper class which can be hashed as expected.
