##Instructions for obtaining grid certificate

###Applying for grid certificate through UK portal
- Go [here](https://portal.ca.grid-support.ac.uk/caportal/)
- Request new User Certificate
- Follow instructions

<strong>For PIN, use an easy memorable passphrase</strong>
- only used for identification, so do not need to remember beyond talking to your RA

*For Bristol people:*
- Your Institution: Bristol IS (Bristol Physics is outdated, IS = "Information Services")
- Talk to [Winnie Lacesso](Winnie.lacesso@bristol.ac.uk) (or [Ian Stewart](I.Stewart@bristol.ac.uk)) to have it approved
- Paste both halves of the certificate in the boxes as instructed on the webpage (including headers) to generate certificate

###Installing certificate on computer
- Install [Certificate Wizard](http://www.ngs.ac.uk/ukca/certificates/certwizard) on ngs website
- Import certificate (make sure it is backup up to a few places)
- Click install

###Importing certificate into Firefox browser
- Go to Preferences->Advanced->Certificates->View Certificates
- Go to 'Your Certificates', and import .p12 file.
- This will allow you to join the ILC Virtual Organisation (VO)

###Register for ILC Virtual Organisation (VO)
- Go [here](https://grid-voms.desy.de:8443/voms/ilc/register/start.action)
- Browser will complain that it is unsafe but just ignore it / make an exception
- Accept its request to validate security certificate
- Fill in information
- Confirm email address

<strong>IMPORTANT:</strong>
You must send off extra information for verification. This is specified in the terms and conditions box at the bottom of the page.

*For Bristol people:*
- Working Group: Bristol Particle Physics
- Wait for acception

###Instructions for ILC DIRAC registration:
- Email ilcdirac-register@cern.ch with name, institution, supervisor, project

<strong>All permissions are now on your certificate so you can use ILC-DIRAC.</strong>

##Setting up LXplus

###Instructions for installing your grid certificate on LXplus
- Need to copy $HOME/.globus on local machine to LXplus account
- Use eg. rsync -avz ~/.globus USERNAME@lxplus.cern.ch:~/.globus where USERNAME is your personal username

<strong>You can now use ILC DIRAC as explained in RunILC-DIRAC.md</strong>
