echo "Setting up lxplus enviroment for pyLCIO/pyROOT"
export ROOTSYS="/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-07/root/5.34.30"
export LCIO="/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-07/lcio/v02-06"
export PYTHONDIR="/usr/lib/python2.6/site-packages"
export LD_LIBRARY_PATH=$ROOTSYS/lib:$PYTHONDIR/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$ROOTSYS/lib:$PYTHONPATH
export PYTHONPATH=:$LCIO/src/python:$PYTHONPATH
echo "Done"