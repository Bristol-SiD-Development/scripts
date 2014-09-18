<strong> You need to change the line "/afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/stdhep-reco-script.py" so it points at the location you've cloned the repo! </strong>

This parallelises the use of the sim-reco chain by splitting the input stdhep file over several LXbatch jobs. It writes a batch submission script for each job to disk and submits it to your chosen queue withe the bsub command.

The paths to the final output files are written to a file as well so they may be recombined using the "lcio_merge_files" program provided by lcio.

If you're on afs then you'll need to source the script at the following location before you have access to this command:

/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05/init_ilcsoft.sh

The script writes the locations of it's output files to a file in the output directory. Using xargs and lcio_merge_files you can quickly recombine all the output into one file.
