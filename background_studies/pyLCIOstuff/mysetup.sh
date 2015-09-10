export ROOTSYS=/Users/mt15801/root
export PATH=$PATH:$ROOTSYS/bin
source $ROOTSYS/bin/thisroot.sh
export LCIO=/Users/mt15801/lcio/trunk/
export LD_LIBRARY_PATH=$LCIO/lib:$ROOTSYS/lib
export PYTHONDIR=/usr/lib/python2.6/site-packages
export PYTHONPATH=$LCIO/src/python:$PYTHONPATH
echo "Done"
