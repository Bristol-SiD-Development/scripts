#! /bin/bash

ilcsoft_version=v01-17-05

ilcsoft_root=/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6

ilcsoft_root_dir=$ilcsoft_root/$ilcsoft_version

echo "Sourcing init_ilcsoft.sh..."
source $ilcsoft_root_dir/init_ilcsoft.sh

/afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/stdhep-reco-script.py -o /afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/output-2000/ -r 2000 -s /afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/steering_files/ -g /afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/geometry_files/ /afs/cern.ch/user/o/oreardon/public/ilc/pythiaZPolebbbar.stdhep 