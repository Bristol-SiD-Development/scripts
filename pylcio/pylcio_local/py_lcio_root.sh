#!/bin/bash

echo "----Setting up pyROOT and pyLCIO enviroment variables----"
export ROOTSYS=/home/jooosh25/summerInstall/root
export PYTHONDIR=/usr/lib/python2.6/site-packages/
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH
export LCIO=/home/jooosh25/summerInstall/lcio/trunk
export PYTHONPATH=$LCIO/src/python:$PYTHONPATH
echo "----DONE----"