###Preparation for DIRAC
- Make sure you are logged in, via ssh, to LXplus</strong>
- Use the following command to set up environmental variables:
```
source /afs/cern.ch/eng/clic/software/DIRAC/bashrc
```
- Use the following command to obtain a valid DIRAC proxy with the correct user group:
```
dirac-proxy-init --group ilc_user
```
###Correctly store detector geometry files
- Set up a detector geometry zip file in the same manner that sidloi3\_edited.zip is, as found in dirac_examples. 
- Gear file can be ignored unless you are changing magnetic field in the detector

###Store detector geometry on the web
- Follow instructions in SettingUpWebStorage.md using the zip file from the previous stage
- alias.properties can now include a line such as 
```
sidloi3_edited: http://www.cern.ch/SITENAME/sidloi3_edited.zip
```
where SITENAME is the website name

###Running an ILC-DIRAC script
- Use python to run an existing python API script for dirac; ensure all paths that are specific to your job have been set up; it still contains my own file paths
- There are three main scripts that can be run at the moment:

<strong>Simple run script - SiDChainJobSimple.py</strong>
- Definitely make this first script you see / run!
- Here, only a single job is sent off with a specified stdhep file, number of events and possibility of output to the grid.
- Contains useful documentation (through comments) to point out strange features of running ILC Dirac.
- Most things hard coded, such as detector geometries and steering files
- Use the following command to run this:
```
python SiDChainJobSimple.py -n 5 --file="/ilc/user/FILEPATH"
```
where filepath refers to a stdhep file in your personal grid storage area. See UsefulDiracCommands.md for uploading files to the grid

<strong>Original script - SiDChainJobOriginal.py</strong>
- This is code originally made by Christian Grefe that was found through [this guide](https://confluence.slac.stanford.edu/display/ilc/Running+LCSim+Analysis+Jobs+on+the+Grid+with+DIRAC)
- Has a number of bugs and other strange things; suggest you completely rehaul code using the simplified multiple job script instead, but refer here for eg. background overlay

<strong>Simplified multiple job script - SiDChainJobReducedMultiple.py</strong>
- This will run a cut-down version of the original script as written by Christian Grefe. There are no background effects and potentially useful code not currently in use has been removed, as well as certain error corrections.
- Good starting point for a complete script that has proper control flow as required
- Run with eg:
```
python SiDChainJob2.py -n 5 --process="ProcessName" --file="/ilc/user/FILEPATH" --detector="sidloi3_edited" --pandoradetector="sidloi3_edited"
```

###ILC DIRAC web portal
- It can be found [here](https://ilcdirac.cern.ch/DIRAC/ILC-Production/ilc_user/jobs/JobMonitor/display), and requires the grid certificate to be installed on your browser
- Go to Jobs -> Job monitor on the top left to get a view of every job currently in operation, sorted by group, date etc.
- Can delete jobs or resend them etc. Make sure you do not edit files before resending, however!
- Can be used to download output sandbox if < 10MB
