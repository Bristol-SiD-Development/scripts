#-------------------------------------------------------------
# Environment variables to enable root
#-------------------------------------------------------------
export ILCSOFT_PATH=/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05
export ROOTSYS=$ILCSOFT_PATH/root/5.34.10
source $ROOTSYS/bin/thisroot.sh
export PATH=$ROOTSYS/bin:$PATH
 
#-----------------------------------------------------
# Environment variables to enable the pylcio module(s)
#-----------------------------------------------------
export LCIO=$ILCSOFT_PATH/lcio/v02-04-03
export PYTHONPATH=$LCIO/src/python:$PYTHONPATH

#-----------------------------------------------------
# Environment variables to enable LCIO file reading in ROOT
#-----------------------------------------------------
export LD_LIBRARY_PATH=$LCIO/lib:$ROOTSYS/lib:$LD_LIBRARY_PATH
