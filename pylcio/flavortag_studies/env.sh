#!/bin/bash

export ILCSOFT_PATH=/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05
export ROOTSYS=$ILCSOFT_PATH/root/5.34.10
export PYTHONDIR=/usr/lib/python2.6/site-packages
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH

export LCIO=$ILCSOFT_PATH/lcio/v02-04-03
export PYTHONPATH=$LCIO/src/python:$PYTHONPATH

echo "Done"