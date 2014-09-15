#!/bin/env python

###
#  Basic job run with only a few input options. Based on a script written by Christian Grefe,
#  christian.grefe@cern.ch
##

from DIRAC.Core.Base import Script
import sys

# Application versions
slicPandoraVer = 'ILC_DBD'
lcsimVer = '2.5'
slicVer = 'v3r0p3'
marlinVer = '0116'

# slic macro. See default for most simple version possible
macroFile = 'slicMacros/default.mac'

# Can use sidloi3 (or any other standard detector) without issue; it will access lcsim web portal
detector = 'sidloi3_edited'

# Appears to use zip file or folder in the grid node's directory. Can also directly specify xml file
slicPandoraDetector = 'sidloi3_edited'

# In script with multiple job ability, it will send out nJobs*nEvts total events, for each input LFN
nEvts = -1

settingsFile = 'pandoraSettings/sid_dbd_pandoraSettings.xml'
# Specifies queue to be used
cpuLimit = 100000
# All ILC Dirac applications require this option
systemConfig = 'x86_64-slc5-gcc43-opt'
# Is wise to change depending on output file size. CERN-SRM can be accessed from castor staging, RAL-SRM is local (UK) SE. Used for >100MB
# CERN-DIP-3 is optimised for smaller files, but has limited space, so use only for library files. Can use dirac-wms-job-get-output-data in lxplus for output as well
storageElement = 'CERN-SRM'
# If no absolute path given, this appears to base its paths on the working directory of the grid node
aliasFile = 'alias.properties'
# Steering files
xmlPrePandora = 'lcsimSteeringFiles/sid_dbd_prePandora_noOverlay.xml'
xmlPostPandora = 'lcsimSteeringFiles/sid_dbd_postPandora.xml' # always use the overlay version to create the selected PFO files
marlinXml = 'marlinSteering/sid_dbd_vertexing.xml'
strategyFile = 'trackingStrategies/sidloi3_trackingStrategies_default.xml'
# python file with an array of grid sites not to operate on
banlistFile = 'bannedSites.py'
# Only provides magnetic field so no need to change...
gearFile = 'gearFiles/sidloi3.gear'
# Gives lfn of input .stdhep file, eg. /ilc/user/m/mgaughra/inputFiles/myfile.stdhep
lfnFile = None
# Specifies an exact grid node to use
destination = None
# Can store output on the grid if this is True
storeOutput = False

Script.registerSwitch( 'f:', 'file=', 'define a single lfn file as input' )
Script.registerSwitch( 'n:', 'events=', 'number of events per job, -1 for all in file (default %s)'%(nEvts) )
Script.registerSwitch( 'O', 'output', 'Stores the output files on the grid at the specified storage element: %s'%(storageElement) )

Script.parseCommandLine()
switches = Script.getUnprocessedSwitches()

for switch in switches:
    opt = switch[0]
    arg = switch[1]
    if opt in ('f','file'):
        lfnFile = arg
    if opt in ('n','events'):
        nEvts = int(arg)
    if opt in ('O','output'):
        storeOutput = True

from ILCDIRAC.Interfaces.API.NewInterface.Applications import *
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.DiracILC import *
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

fileCatalog = FileCatalogClient()

# list of files used as input to the job
inputSandbox = []

# slicPandora deletes the 
inputSandbox.append( ['LFN:/ilc/prod/software/lcsim/lib.tar.gz'] )

outputSandbox = [ "*.log", "*.xml", "*.lcsim", "*.slcio" ]

# read file with list of banned sites
f = open( banlistFile, 'r')
exec(f.read())

# You can either use a group name for the job to link outputs, or alternatively use a separate repository file for each job so that you can
# retrieve all jobs associated with the file at once with a single command (eg. dirac-repo-retrieve-jobs-output RepositoryFile)
repositoryFile = "repositoryFiles/RepositoryFile"

# The True indicates that a repository file is included
dirac = DiracILC ( True , repositoryFile )

inputFile =  'LFN:' + lfnFile 
inputFile = inputFile.replace( 'LFN:', '' )

# base name for all application output files
outputFile = "output"

slicOutput='slic.slcio'
lcsimOutput='prePandora.slcio'
slicPandoraOutput='slicPandora.slcio'

# Storage path is based on your home directory on the grid. Eg. /ilc/user/u/username
storagePath = "output/test"

# We will only ever run a user job
job = UserJob()

# Setting up SLIC application
slic = SLIC()
slic.setVersion( slicVer )
slic.setSteeringFile( macroFile )
slic.setNumberOfEvents( nEvts )
slic.setStartFrom( 0 )
slic.setDetectorModel( detector )
slic.setOutputFile( slicOutput )
result = job.append( slic )
if not result['OK']:
    # job.append will return an error message if your application object is not properly initialised
    print result['Message']
    sys.exit(2)

# Setting up first lcsim run
lcsim = LCSIM()
lcsim.setVersion( lcsimVer )
# This will use the output file from slic in lcsim
lcsim.getInputFromApp( slic )
lcsim.setNumberOfEvents( nEvts )
lcsim.setSteeringFile( xmlPrePandora )
lcsim.setAliasProperties( aliasFile )
lcsim.setDetectorModel( detector + '.zip' )
lcsim.setTrackingStrategy( strategyFile )
lcsim.setOutputFile( lcsimOutput )
result = job.append( lcsim )
if not result['OK']:
    print result['Message']
    sys.exit(2)

# Setting up slicPandora to run
slicPandora = SLICPandora()
slicPandora.setVersion( slicPandoraVer )
slicPandora.setDetectorModel( slicPandoraDetector )
slicPandora.setPandoraSettings( settingsFile )
slicPandora.getInputFromApp( lcsim )
slicPandora.setNumberOfEvents( nEvts )
slicPandora.setStartFrom( 0 )
slicPandora.setOutputFile( slicPandoraOutput )
result = job.append( slicPandora )
if not result['OK']:
    print result['Message']
    sys.exit(2)

# Marlin for LCFI vertex fitting
vertexing = Marlin()
vertexing.setVersion( marlinVer )
vertexing.setSteeringFile( marlinXml )
vertexing.setGearFile( gearFile )
vertexing.getInputFromApp( slicPandora )
vertexing.setOutputFile( outputFile + '.slcio' )
result = job.append( vertexing )
if not result['OK']:
    print result['Message']
    sys.exit(2)

# Final lcsim stage
lcsimFinalize = LCSIM()
lcsimFinalize.setVersion( lcsimVer )
lcsimFinalize.getInputFromApp( vertexing )
lcsimFinalize.setNumberOfEvents( nEvts )
lcsimFinalize.setSteeringFile( xmlPostPandora )
lcsimFinalize.setAliasProperties( aliasFile )
lcsimFinalize.setDetectorModel( detector + '.zip' )
lcsimFinalize.setOutputRecFile( outputFile+'_REC.slcio' )
lcsimFinalize.setOutputDstFile( outputFile+'_DST.slcio' )
result = job.append( lcsimFinalize )
if not result['OK']:
    print result['Message']
    sys.exit(2)

job.setOutputSandbox ( outputSandbox )
job.setInputSandbox ( inputSandbox )

# This appears to send the input data file into the first program in the list; here it is SLIC
job.setInputData( [ inputFile ] )

# Add the two files created in the final lcsim stage to the output data (retrieved using eg. dirac-wms-job-get-output-data)
outputData = []
outputData.append( outputFile+'_REC.slcio' )
outputData.append( outputFile+'_DST.slcio' )

# Can store data on the grid using the specified storage element
if storeOutput == True:
    job.setOutputData ( outputData, storagePath, storageElement )

# This sets the queue for the job to be run
job.setCPUTime( cpuLimit )

job.setSystemConfig ( systemConfig )

# Job name allows for easy identification
job.setName ( "JobName" )

# Use groups for related jobs. As with name, dirac does not care about this
job.setJobGroup( "JobGroup" )

# We use a banlist (bannedSites.py) but a destination can be directly specified. If automatic, it appears to use geographically closer grid nodes (manchester etc.)
if destination:
    job.setDestination( destination )
else:
    job.setBannedSites( bannedSites )


job.submit ( dirac )

