##SiD Chain With Flavortagging

Script for submitting jobs to ILC-DIRAC, can split large input files into many smaller jobs. Tried to add flavortagging capability...

Currently unable to achieve this as can't find a way to ship the lcfiweights folder via the input sandbox to the node working directory. As LCFIPlus requires the input of a "weightDirectory" and not individual files, a directory is required. Therefore, currently unable to run flavortagging. 

However, the rest of the script works well submitting jobs without flavortagging (Produces DST outputs). Usage...

```
python SiDChainJobWithFlavortag.py LFNPathToStdhepInput.stdhep -r totalNumberOfEventsToRun -s SplitTotalIntoJobsOfThisSize -o outputPathOnGrid --dontPromptMe
```

Use --help to see all the options. -f includes flavortagging. You need to upload pandoraSettings.xml to the grid and then change the path in the script, slicPandora has issues taking its settings from a local file.

Another problem has to be corrected for. The xml parser that ILC-DIRAC uses when checking Marlin steeringFiles does not allow for "&&", which is present in any of the steering files related to flavortagging. Therefore need to use "&amp;&amp;" instead, which is the tinyxml equivalent, and allows the .xml file to be accepted. It then appears to convert them back to "&&" which LCFIPlus should accept. However, have never been able to run LCFIPlus this far due to problem explained above to check this!!!

###PROBLEMS 

see [here](https://jira.slac.stanford.edu/browse/MAR-55) and [here](https://github.com/DIRACGrid/DIRAC/issues/1161)!!!
