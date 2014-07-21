#! /bin/bash

#LSF_LOGON_DESKTOP=1
#LSB_TSJOB=1

ilcsoft_version=v01-17-05

ilcsoft_root=/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6

ilcsoft_root_dir=$ilcsoft_root/$ilcsoft_version

echo "Sourcing init_ilcsoft.sh..."
source $ilcsoft_root_dir/init_ilcsoft.sh

slic_binary=$ilcsoft_root_dir/slic/v03-01-03/build/bin/slic
lcsim_jar=/afs/cern.ch/eng/clic/software/lcsim/lcsim-2_5/target/lcsim-2.5-bin.jar
pandora_binary=$ilcsoft_root_dir/slicPandora/v01-00-00/build/bin/PandoraFrontend
marlin_binary=$ilcsoft_root_dir/Marlin/v01-05/bin/Marlin
anajob_binary=$ilcsoft_root_dir/lcio/v02-04-03/bin/anajob

echo "Running slic simulation..."

$slic_binary -g /afs/cern.ch/user/o/oreardon/public/ilc/simulation/detectors/sidloi3/sidloi3.lcdd \
-i /afs/cern.ch/user/o/oreardon/public/ilc/pythiaZPolebbbar.stdhep \
-o /cern.ch/user/o/oreardon/public/ilc/simulation/pythiaZPolebbbar_slic-3.1.3_geant4-v9r6p1_QGSP_BERT_sidloi3.slcio \
-p /afs #/cern.ch/user/o/oreardon/public/ilc/simulation \
-r 10 \
-P /afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05/slic/v03-01-03/simulation/particle.tbl

#$slic_binary /afs/cern.ch/user/o/oreardon/public/ilc/macro/stdhep.macro

if [ "$?" -ne "0" ]; then
  exit 1
fi

                   
input="/afs/cern.ch/user/o/oreardon/public/ilc/simulation/pythiaZPolebbbar_slic-3.1.3_geant4-v9r6p1_QGSP_BERT_sidloi3.slcio"
input_no_ext=${input%.*}

echo $input_no_ext

lcsim_1_input=$input
lcsim_1_output=$input_no_ext"_lcsim1.slcio"

echo $lcsim_1_output

echo "Running lcsim prePandora reco"
java -jar $lcsim_jar /afs/cern.ch/user/o/oreardon/public/ilc/myscripts/sid_dbd_prePandora_noOverlay.xml -DinputFile=$lcsim_1_input -DtrackingStrategies=/afs/cern.ch/user/o/oreardon/public/ilc/myscripts/sidloi3_trackingStrategies_default.xml -DoutputFile=$lcsim_1_output

if [ "$?" -ne "0" ]; then
  exit 1
fi


#We'll need to restore the old version so marlin works
old_LD_LIBRARY_PATH=$LD_LIBRARY_PATH
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ilcsoft_root_dir/slicPandora/v01-00-00/build/lib/

pandora_output="/afs/cern.ch/user/o/oreardon/public/ilc/simulation/pythiaZPolebbbar_slic-3.1.3_geant4-v9r6p1_QGSP_BERT_sidloi3_pandora.slcio"

echo "Runing pandora..."
$pandora_binary -g /afs/cern.ch/user/o/oreardon/public/ilc/myscripts/sidloi3_pandora.xml -c /afs/cern.ch/user/o/oreardon/public/ilc/myscripts/sid_dbd_pandoraSettings.xml -i $lcsim_1_output -o $pandora_output


if [ "$?" -ne "0" ]; then
  exit 1
fi

#cp ../myscripts/sid_dbd_vertexing.xml .
#emacs sid_dbd_vertexing.xml #make changes as shown at https://confluence.slac.stanford.edu/display/~stanitz/From+Zero+to+SiD+-+Running+Sim+Reco

#Clean out the crap we've put in $LD_LIBRARY_PATH. Marlin complained about duplicate libraries.
LD_LIBRARY_PATH=$old_LD_LIBRARY_PATH

echo "Running marlin.."
$marlin_binary /afs/cern.ch/user/o/oreardon/public/ilc/simulation/BB_sid_dbd_vertexing.xml 
#$marlin_binary /afs/cern.ch/user/o/oreardon/public/ilc/data/stearingFiles/v02_p01/flavortag.xml
if [ "$?" -ne "0" ]; then
  exit 1
fi


lcsim_2_input="pythiaZPolebbbar_slic-3.1.3_geant4-v9r6p1_QGSP_BERT_sidloi3_lcfi.slcio"
lcsim_2_recFile="pythiaZPolebbbar_slic-3.1.3_geant4-v9r6p1_QGSP_BERT_sidloi3_full.slcio"
lcsim_2_dstFile="pythiaZPolebbbar_slic-3.1.3_geant4-v9r6p1_QGSP_BERT_sidloi3_dst.slcio"

echo "Running second lcsim reco..."
java -jar $lcsim_jar ../myscripts/sid_dbd_postPandora.xml -DinputFile=$lcsim_2_input -DrecFile=$lcsim_2_recFile -DdstFile=$lcsim_2_dstFile


if [ "$?" -ne "0" ]; then
  exit 1
fi

echo "Running anajob ..."
$anajob_binary $lcsim_2_recFile

if [ "$?" -ne "0" ]; then
  exit 1
fi

#JAS3 doesn't seem to work...