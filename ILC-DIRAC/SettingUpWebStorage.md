##Setting up web storage
As slicPandora deletes geometry zip files (for no good reason), you will have to upload the detector geometry zip file to a web server; this will allow access for lcsim
###Setting up folder structure
- Create a new folder "www" in your home directory in afs (all 
- Create a new folder "SITENAME" in this directory.
<strong>website name must begin with "test-" if you wish to create a test website, which prevents search engine listings and restricts outside access. THe name may contain numbers, letters and hyphens (-) only </strong>
- Set up the Access Control List permissions for this folder such that the cern web server can read it; eg from ~/www/ type:
```
  fs setacl -dir SITENAME -acl webserver:afs rl 
```
- The directory SITENAME need not necessarily be the exact name of the website; it simply helps with clarity. You will set the directory used when setting up the website (in the following section)
###Creating website
- Go to your cern account page [here](https://account.cern.ch/account/Management/MyAccounts.aspx)
- Go to Sevices -> Web Services and select "Create a new website"
- Fill in as follows:
Category: Test Site
Site name: SITENAME (including "test-" at start)
Description: Anything
Site type: AFS folder
Path: /afs/cern.ch/user/u/username/www/SITENAME
Owner: Leave as is
- Check the box and submit. Everything is now set up!
###Uploading zip file to the web server
- Simply copy the zip file into the folder ~/www/SITENAME
- Everything is now accessible through eg:
http://www.cern.ch/SITENAME/sidloi3_edited.zip

