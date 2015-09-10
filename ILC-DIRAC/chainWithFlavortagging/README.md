##SiD Chain With Flavortagging

Script for submitting jobs to ILC-DIRAC, can split large input files into many smaller jobs. Tried to add flavortagging capability...

Currently unable to achieve this as can't find a way to ship the lcfiweights folder via the input sandbox to the node working directory. As LCFIPlus requires the input of a "weightDirectory" and not individual files, a directory is required. Therefore, currently unable to run flavortagging. 

However, the rest of the script works well submitting jobs without flavortagging (Produces DST outputs). Usage...

```
python SiDChainJobWithFlavortag.py LFNPathToStdhepInput.stdhep -r totalNumberOfEventsToRun -s SplitTotalIntoJobsOfThisSize -o outputPathOnGrid --dontPromptMe
```

Use --help to see all the options. -f includes flavortagging. You need to upload pandoraSettings.xml to the grid and then change the path in the script, slicPandora has issues taking its settings from a local file.

###PROBLEMS 

see [here](https://jira.slac.stanford.edu/browse/MAR-55) and [here](https://github.com/DIRACGrid/DIRAC/issues/1161)!!!
