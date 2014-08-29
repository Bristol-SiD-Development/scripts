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

###Set up web storage for detector geometry files
- Ensure that 

###Running an ILC-DIRAC script
- Use python to run an existing python API script for dirac
- There are three main scripts that can be run at the moment

<strong>Simple run script</strong>
- Here, only a single job is sent off with a specified stdhep file, number of events and possibility of output to the grid.
- Contains useful documentation to point out strange features of running ILC Dirac
- Use the following command to run this:

```
    python SiDChainJobSimple.py -n 5 --file="/ilc/user/FILEPATH"
```
where filepath refers to a stdhep file in your personal afs space.

<strong>Simplified multiple job script</strong>
- This will run a ver
