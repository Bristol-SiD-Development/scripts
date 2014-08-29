## General problems with using ILC Dirac
- If sending off multiple jobs, there may be a delay between the job submission and the input being sent to the grid. Any edits after submission may be included!
- When completing the full Sim-Reco chain, if using a local zip file for lcsim slicPandora will delete it before it gets to the second lcsim stage. Make sure that you upload the zip file to a website (as described in SettingUpWebStorage.md)
- Make sure you include all files specified in the python script. Eg. macro file is not necessary when running SLIC outside of ILC DIRAC; here, however, it is necessary and is not empty
