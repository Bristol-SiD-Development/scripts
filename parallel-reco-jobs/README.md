This parallelises the use of the sim-reco chain by splitting the input stdhep file over severa LXbatch jobs. It writes a batch submission script for each job to disk and submits it to your chosen queue withe the bsub command.

The paths to the final output files are written to a file as well so they may be recombined using the "lcio_merge_files" program provided my lcio.