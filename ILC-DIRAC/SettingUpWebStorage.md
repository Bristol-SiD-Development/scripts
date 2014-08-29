##Setting up web storage
As slicPandora deletes geometry zip files (for no good reason), you will require access to the detector geometry from a zip file on a web server; this will allow access for lcsim
###Setting up folder structure
- Create a new folder "www" in your home directory in afs (all websites are based in this folder)
- Create a new folder "DIRNAME" in this directory.

- Set up the Access Control List permissions for this folder such that the cern web server can read it; eg from ~/www/ type:
```
fs setacl -dir DIRNAME -acl webserver:afs rl 
```
###Creating website
- Go to your cern account page [here](https://account.cern.ch/account/Management/MyAccounts.aspx)
- Go to Sevices -> Web Services and select "Create a new website"
- Fill in as follows:

Category: Test Site

Site name: SITENAME (including "test-" at start)

Description: Anything

Site type: AFS folder

Path: /afs/cern.ch/user/u/username/www/DIRNAME

Owner: Leave as is

<strong>website name SITENAME must begin with "test-" if you wish to create a test website, which prevents search engine listings and restricts outside access. The name may contain numbers, letters and hyphens (-) only </strong>

- Check the box and submit. Everything is now set up!
###Uploading zip file to the web server
- Simply copy the zip file into the folder ~/www/DIRNAME
- Everything is now accessible through eg:

http://www.cern.ch/SITENAME/sidloi3_edited.zip
