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

###Running an ILC-DIRAC script
- Use python to run an existing python API script for dirac
