#!/bin/python

###
#  Convenience script for submitting jobs with full reconstruction chain (or parts of it) to DIRAC
#  christian.grefe@cern.ch
##

from DIRAC.Core.Base import Script
import sys

# default parameters
macroFile = 'slicMacros/defaultClicCrossingAngle.mac'
macroFile = 'slicMacros/default.mac'
slicPandoraVer = 'ILC_DBD'
lcsimVer = '2.5'
slicVer = 'v3r0p3'
marlinVer = '0116'
detector = 'sidloi3'
jobTitle = 'fullReco'
inputFileList = None
nEvts = -1
nJobs = 1
settingsFile = 'pandoraSettings/sid_dbd_pandoraSettings.xml'
cpuLimit = 100000
mergeSlcioFiles = 1
slicPandoraPath = 'LFN:/ilc/prod/software/slicpandora/'
slicPandoraDetector = detector
lcsimPath = 'LFN:/ilc/prod/software/lcsim/'
systemConfig = 'x86_64-slc5-gcc43-opt'
storageElement = 'RAL-SRM'
aliasFile = 'alias.properties'
xmlFile = 'lcsimSteeringFiles/sid_dbd_prePandora_noOverlay.xml'
xmlPostPandora = 'lcsimSteeringFiles/sid_dbd_postPandora.xml' # always use the overlay version to create the selected PFO files
marlinXml = 'marlinSteering/sid_dbd_vertexing.xml'
lcsimTemplate = ''
strategyFile = 'trackingStrategies/sidloi3_trackingStrategies_default.xml'
banlistFile = 'bannedSites.py'
gearFile = 'gearFiles/%s.gear'%(detector)
overlayBX = 0
overlayWeight = 3.2
maxFiles = -1
lfnlist = None
lfnFile = None
prodID = None
process = None
debug = True
debugOld = False
agentMode = False
destination = None
energy = 1000
preDefinedSetup = None
dataType = ''
lfnProdPath='/ilc/prod/'

Script.registerSwitch( 'a:', 'alias=', 'name of the alias.properties file to use (default %s)'%(aliasFile) )
Script.registerSwitch( 'A', 'agent', 'Submits the job in agent mode, which will run the job on the local machine' )
Script.registerSwitch( 'b:', 'banlist=', 'file with list of banned sites (default %s)'%(banlistFile) )
Script.registerSwitch( 'C:', 'destination=', 'jobs are only submitted to the given site (default %s)'%(destination) )
Script.registerSwitch( 'D:', 'detector=', 'name of the detector model (default %s)'%(detector) )
Script.registerSwitch( 'f:', 'file=', 'define a single lfn file as input' )
Script.registerSwitch( 'F:', 'config=', 'Pre-defined configuration (default %s)'%(preDefinedSetup) )
Script.registerSwitch( 'i:', 'input=', 'input python script holding the lfnlist to process' )
Script.registerSwitch( 'I:', 'prodid=', 'use a production id to define the input lfnlist' )
Script.registerSwitch( 'l:', 'lcsimxml=', 'lcsim steering xml template (default %s)'%(xmlFile) )
Script.registerSwitch( 'L:', 'lcsim=', 'lcsim version to use (default %s)'%(lcsimVer) )
Script.registerSwitch( 'j:', 'jobs=', 'number of jobs that each input file gets split into (default %s)'%(nJobs) )
Script.registerSwitch( 'm:', 'macro=', 'name of the macro file used for SLIC (default %s)'%(macroFile) )
Script.registerSwitch( 'M:', 'merge=', 'number of slcio input files used per job, only used if no slic step (default %s)'%(mergeSlcioFiles) )
Script.registerSwitch( 'n:', 'events=', 'number of events per job, -1 for all in file (default %s)'%(nEvts) )
Script.registerSwitch( 'O:', 'overlay=', 'number of bunch crossings overlaid over each event (default %s)'%(overlayBX) )
Script.registerSwitch( 'w:', 'overlayweight=', 'number of gg->hadron interactions per bunch crossing (default %s)'%(overlayWeight) )
Script.registerSwitch( 'p:', 'process=', 'process name to be used for naming of path etc.' )
Script.registerSwitch( 'P:', 'pandora=', 'slicPandora version to use (default %s)'%(slicPandoraVer) )
Script.registerSwitch( 'S:', 'slic=', 'slic version (default %s)'%(slicVer) )
Script.registerSwitch( 't:', 'time=', 'CPU time limit per job in seconds (default %s)'%(cpuLimit) )
Script.registerSwitch( 'T:', 'title=', 'job title (default %s)'%(jobTitle) )
Script.registerSwitch( 'v', 'verbose', 'switches off the verbose mode' )
Script.registerSwitch( 'k:', 'marlinxml=', 'name of marlin steering file (default %s)'%(marlinXml) )
Script.registerSwitch( 'K:', 'marlin=', 'Marlin version to use (default %s)'%(marlinVer) )
Script.registerSwitch( 'x:', 'settings=', 'name of pandora settings file (default %s)'%(settingsFile) )
Script.registerSwitch( 'y:', 'strategy=', 'name of tracking strategy file to use (default %s)'%(strategyFile) )
Script.registerSwitch( 'z:', 'maxfiles=', 'maximum number of files to process (default %s)'%(maxFiles) )
Script.registerSwitch( 'g:', 'pandoradetector=', 'name of pandora geometry xml file or just detector name (default %s)'%(slicPandoraDetector) )
Script.registerSwitch( 'G:', 'gearxml=', 'name of gear geometry xml file (default %s)'%(gearFile) )
Script.registerSwitch( 'Z:', 'postlcsimxml=', 'name of the lcsim steering file used in the finalization step (default %s)'%(xmlPostPandora) )
Script.registerSwitch( 'Y:', 'datatype=', 'data type used for input from a production ID (default %s)'%(dataType) )

Script.setUsageMessage( sys.argv[0]+'-n <nEvts> (-i <inputList> OR -I <prodID> AND/OR -m <macro>) (<additional options>)\\A process name needs to be defined using -p NAME for the output path. Only when using a production ID as input the process name can be obtained from the file catalog meta data.' )

Script.parseCommandLine()
switches = Script.getUnprocessedSwitches()

for switch in switches:
    opt = switch[0]
    arg = switch[1]
    if opt in ('a','alias'):
        aliasFile = arg
    if opt in ('A','agent'):
        agentMode = True
    if opt in ('b','banlist'):
        banlistFile = arg
    if opt in ('C','destination'):
        destination = arg
    if opt in ('D','detector'):
        detector = arg
    if opt in ('f','file'):
        lfnFile = arg
    if opt in ('F','configuration'):
        preDefinedSetup = arg
    if opt in ('i','input'):
        inputFileList = arg
    if opt in ('I','prodid'):
        prodID = arg
    if opt in ('l','lcsimxml'):
        lcsimTemplate = arg
    if opt in ('L','lcsim'):
        lcsimVer = arg
    if opt in ('j', 'jobs'):
        nJobs = int(arg)
    if opt in ('m','macro'):
        macroFile = arg
    if opt in ('M','merge'):
        mergeSlcioFiles = int(arg)
    if opt in ('n','events'):
        nEvts = int(arg)
    if opt in ('O','overlay'):
        overlayBX = int(arg)
    if opt in ('w','overlayweight'):
        overlayWeight = float(arg)
    if opt in ('p','process'):
        process = arg
    if opt in ('P','pandora'):
        slicPandoraVer = arg
    if opt in ('x','settings'):
        settingsFile = arg
    if opt in ('S','slic'):
        slicVer = arg
    if opt in ('t','time'):
        cpuLimit = arg
    if opt in ('T','title'):
        jobTitle = arg
    if opt in ('y','strategy'):
        strategyFile = arg
    if opt in ('z','maxfiles'):
        maxFiles = int(arg)
    if opt in ('v','verbose'):
        debug = False
    if opt in ('k','marlinxml'):
        marlinXml = arg
    if opt in ('K','marlin'):
        marlinVer = arg
    if opt in ('g','pandoradetector'):
        slicPandoraDetector = arg
    if opt in ('G', 'gearxml'):
        gearFile = arg
    if opt in ('Z','postlcsimxml'):
        xmlPostPandora = arg
    if opt in ('Y','datatype'):
        dataType = arg

if debug:
    print ''
    print '################################'
    print ' SiD job submission to DIRAC'
    print '        christian.grefe@cern.ch'
    print '################################'
    print ''

if not inputFileList and not prodID and not lfnFile:
    if macroFile == 'slicMacros/default.mac':
        Script.showHelp()
        sys.exit(2)
        
if not process and not prodID:
    Script.showHelp()
    sys.exit(2)
        
if overlayBX > 0:
    if not lcsimTemplate:
        xmlFile = 'lcsimTemplates/sid_dbd_prePandora.xml'
    #xmlPostPandora = lcsimPath+'clic_cdr_postPandoraOverlay.lcsim'

#preDefinedSetup = ''
#preDefinedSetup = 'CLIC_CDR_3TeV'
#preDefinedSetup = 'CLIC_CDR_1.4TeV'

if not preDefinedSetup:
    pass

elif preDefinedSetup in ['ILC_DBD_1000']:
    energy = 1000
    if slicVer:
        slicVer = 'v3r0p3'
    lcsimVer = '2.5'
    marlinVer = ''
    slicPandoraVer = 'ILC_DBD'
    macroFile = 'slicMacros/defaultIlcCrossingAngle.mac'
    xmlFile = 'lcsimTemplates/sid_dbd_prePandora_noOverlay.xml'
    if overlayBX > 0:
        xmlFile = 'lcsimTemplates/sid_dbd_prePandora.xml'
    xmlPostPandora = 'lcsimTemplates/sid_dbd_postPandoraOverlay.lcsim'
    strategyFile = 'trackingStrategies/sidloi3_trackingStrategies_default.xml'
    settingsFile = 'pandoraSettings/sid_dbd_pandoraSettings.xml'
    detector = 'sidloi3'
    slicPandoraDetector = detector

elif preDefinedSetup in ['ILC_DBD_500']:
    energy = 500
    if slicVer:
        slicVer = 'v3r0p3'
    lcsimVer = '2.5'
    marlinVer = ''
    slicPandoraVer = 'ILC_DBD'
    macroFile = 'slicMacros/defaultIlcCrossingAngle.mac'
    xmlFile = 'lcsimTemplates/sid_dbd_prePandora_noOverlay.xml'
    if overlayBX > 0:
        xmlFile = 'lcsimTemplates/sid_dbd_prePandora_gghad_only.xml'
    xmlPostPandora = 'lcsimTemplates/sid_dbd_postPandoraOverlay.lcsim'
    strategyFile = 'trackingStrategies/sidloi3_trackingStrategies_default.xml'
    settingsFile = 'pandoraSettings/sid_dbd_pandoraSettings.xml'
    detector = 'sidloi3'
    slicPandoraDetector = detector

elif preDefinedSetup in ['CLIC_CDR_3000']:
    energy = 3000
    slicVer = 'v2r9p8'
    lcsimVer = 'CLIC_CDR'
    marlinVer = ''
    slicPandoraVer = 'CLIC_CDR'
    macroFile = 'slicMacros/defaultClicCrossingAngle.mac'
    xmlFile = 'lcsimTemplates/clic_cdr_prePandora.lcsim'
    if overlayBX > 0:
        xmlFile = 'lcsimTemplates/clic_cdr_prePandoraOverlay_3000.0.lcsim'
    xmlPostPandora = 'lcsimTemplates/clic_cdr_postPandoraOverlay.lcsim'
    strategyFile = 'trackingStrategies/defaultStrategies_clic_sid_cdr.xml'
    settingsFile = 'pandoraSettings/clic_cdr_pandoraSettings.xml'
    detector = 'clic_sid_cdr'
    slicPandoraDetector = detector
    
elif preDefinedSetup in ['CLIC_CDR_1400']:
    energy = 1400
    slicVer = 'v2r9p8'
    lcsimVer = 'CLIC_CDR'
    marlinVer = ''
    slicPandoraVer = 'CLIC_CDR'
    macroFile = 'slicMacros/defaultClicCrossingAngle.mac'
    xmlFile = 'lcsimTemplates/clic_cdr_prePandora.lcsim'
    if overlayBX > 0:
        xmlFile = 'lcsimTemplates/clic_cdr_prePandoraOverlay_1400.0.lcsim'
    xmlPostPandora = 'lcsimTemplates/clic_cdr_postPandoraOverlay.lcsim'
    strategyFile = 'trackingStrategies/defaultStrategies_clic_sid_cdr.xml'
    settingsFile = 'pandoraSettings/clic_cdr_pandoraSettings.xml'
    detector = 'clic_sid_cdr'
    slicPandoraDetector = detector
    
else:
    print 'Unknown predefined configuration %s'%(preDefinedSetup)


# helper function to replace strings in a textfile
def prepareFile( fileNameTemplate, fileNameOut, replacements ):
    f = open(fileNameTemplate)
    txt = f.read()
    counter = []
    for repkey,reprep in replacements:
        counter.append( ( repkey, reprep, txt.count(repkey) ) )
        txt = txt.replace( repkey, reprep )
    fOut = open( fileNameOut, "w" )
    fOut.write( txt )
    return counter

from ILCDIRAC.Interfaces.API.NewInterface.Applications import *
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import *
from ILCDIRAC.Interfaces.API.DiracILC import *
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient

fileCatalog = FileCatalogClient()

# list of files used as input to the job
inputSandbox = []

# tracking strategies
#inputSandbox.append( 'LFN:/ilc/prod/software/lcsim/trackingStrategies/'+detector+'/'+strategyFile )
#inputSandbox.append( 'LFN:/ilc/prod/software/lcsim/trackingStrategies/'+detector+'/clic_sid_cdr_strategy_5hits_10chisq.xml' )

# JNI bindings for root writer
if lcsimVer:
    inputSandbox.append( 'LFN:/ilc/prod/software/lcsim/lib.tar.gz' )

outputSandbox = [ "*.log", "*.xml", "*.lcsim" ]

# read file with list of banned sites
if banlistFile:
    f = open( banlistFile, 'r')
    exec(f.read())
if not bannedSites:
    bannedSites = ['']

if lcsimVer and overlayBX > 0:
    jobTitle += '_%sBXbackground'%(overlayBX)
repositoryFile = 'repositoryFiles/'+detector+'.'+jobTitle.replace('/', '.')+'.'

# create a repository file and generate list of lfns to process
if prodID:      # use a production id to define the lfnlist
    meta = {}
    meta[ 'ProdID' ] = prodID
    if dataType:
        meta['Datatype'] = dataType
    print 'Using production ID to define LFN list:'
    result = fileCatalog.getCompatibleMetadata( meta, lfnProdPath )
    if not result['OK']:
        print "Error looking up the file catalog for metadata"
        sys.exit(2)
    metaData = result['Value']
    print '  Found production ID %s. Associated meta data:'%( prodID )
    for key, value in metaData.iteritems():
        if not len(value) == 0:
            print '    %s: %s'%( key, value[0] )
    if metaData['Datatype'][0] == 'SIM':
        slicVer = ''        # data has been simulated, can skip SLIC step
    if metaData['EvtType'] and not process:
        process = metaData['EvtType'][0]
    if slicVer and metaData['NumberOfEvents']:
        if nEvts < 1:
            nEvts = int(metaData['NumberOfEvents'][0])
    result = fileCatalog.findFilesByMetadata( meta, lfnProdPath )
    if not result['OK']:
        print "Error looking up the file catalog for metadata"
        sys.exit(2)
    lfnlist = map(lambda x: "LFN:"+x, result['Value'])    # need to add "LFN:" to each entry
    print '  Found %s files associated with meta data'%( len(lfnlist) )
    print ''
    repositoryFile += 'prod'+prodID+'.cfg'
elif inputFileList:     # read a file containing an lfnlist
    repositoryFile += inputFileList.split('/')[-1].replace('.py','.cfg')
    f = open( inputFileList, 'r')
    exec(f.read())
    if not lfnlist:
        print "Error no lfnlist in %s"%(inputFileList)
        sys.exit(2)
elif lfnFile:
    lfnlist = [ 'LFN:' + lfnFile ]
    #Changed
    repositoryFile += "ThatFile"
    #Changed
else:           # no input files, GEANT4 particle source should be defined in slic macro
    repositoryFile += macroFile.split('/')[-1].replace('.mac','.cfg')
    lfnlist = [ '' ]

dirac = DiracILC ( True , repositoryFile )

inputFiles = []
filesProcessed = 0
for inputFile in lfnlist:
    inputSlcios = None
    if filesProcessed == maxFiles:
        break

    filesProcessed += 1
    inputFile = inputFile.replace( 'LFN:', '' )
    
    # processing multiple input files in a single job starting with lcsim
    if lcsimVer and not slicVer:
        inputFiles.append(inputFile)
        if len(inputFiles) < mergeSlcioFiles and filesProcessed != len(lfnlist):
            continue
        inputSlcios = inputFiles
        inputFiles = []
    
    if inputFile:
    
        if slicVer:
            outputFileBase = jobTitle.replace('/','.')+'_'+inputFile.split('/')[-1].replace( '.stdhep', '' )
        else:
            if not lcsimVer:
                inputSlcios = inputFile
                outputFileBase = jobTitle.replace('/','.')+'_'+inputSlcios.split('/')[-1].replace( '.slcio', '' )
            else:
                outputFileBase = jobTitle.replace('/','.')+'_'+inputSlcios[0].split('/')[-1].replace( '.slcio', '' )
    else:
        outputFileBase = jobTitle.replace('/','.')+'_'+macroFile.split('/')[-1].replace('.mac','_%s'%(nEvts))
        if not process:
            print 'ERROR: no process defined. Use -p <processName> to define the storage path'
            sys.exit(2)

    for job in xrange( nJobs ):
        
        outputFile = outputFileBase
        
        if not nJobs == 1:
            outputFile += '_%s'%(job)
        
        if lcsimVer:
            slicOutput='slic.slcio'
        else:
            slicOutput=outputFile+'.slcio'
        
        if slicPandoraVer:
            lcsimOutput='prePandora.slcio'
        else:
            lcsimOutput=outputFile+'.slcio'
            
        if marlinVer:
            slicPandoraOutput='slicPandora.slcio'
        else:
            slicPandoraOutput=outputFile+'.slcio'

        
        storagePath = detector+'/'+process+'/'+jobTitle

        outputData = []
        
        replacements = [
            ( '${outputSlcioFile}', outputFile+'.slcio' ),
            ( '${outputRootFile}', outputFile+'.root' ),
            ( '${outputAidaFile}', outputFile+'.aida' ),
            ( '${trackingStrategyFile}', strategyFile.split('/')[-1] )
        ]
        
        if lcsimTemplate:
            xmlFile = 'lcsimSteeringFiles/'+outputFile + '.xml'
            counter = prepareFile( lcsimTemplate, xmlFile, replacements )
            for key, rep, count in counter:
                if key.count('output') and count:
                    outputData.append( rep )        # add to list of output files if key denotes some output and is present in template
            if slicPandoraVer and lcsimVer:
                outputData.append( outputFile+'_REC.slcio' )
                outputData.append( outputFile+'_DST.slcio' )
        else:
            if slicPandoraVer and lcsimVer:
                outputData.append( outputFile+'_REC.slcio' )
                outputData.append( outputFile+'_DST.slcio' )
            else:
                outputData.append( outputFile+'.slcio' )        # default reco only creates one output file
        
        
        startEvt = job*nEvts
        
        job = UserJob()
        
        if slicVer:
            if nEvts < 0:
                print 'ERROR: need to set number of events per job for SLIC. Use -n <nEvts> to set number of events.'
                sys.exit(2)
            slic = SLIC()
            slic.setVersion( slicVer )
            slic.setEnergy( energy )
            slic.setSteeringFile( macroFile )
            slic.setNumberOfEvents( nEvts )
            slic.setStartFrom( startEvt )
            slic.setDetectorModel( detector )
            slic.setOutputFile( slicOutput )
            result = job.append( slic )
            if not result['OK']:
                print result['Message']
                sys.exit(2)
            
        if lcsimVer:
            if overlayBX > 0:
                if nEvts < 0:
                    print 'ERROR: need to set number of events per job for overlay. Use -n <nEvts> to set number of events.'
                    sys.exit(2)
                if preDefinedSetup in ['CLIC_CDR_3000']:
                    # define input for gghad background overlay
                    gghad = OverlayInput()
                    #gghad.setProdID( 369 )
                    gghad.setEnergy( energy )
                    gghad.setBXOverlay( 60 )
                    gghad.setGGToHadInt( 3.2 )
                    gghad.setNbSigEvtsPerJob( nEvts )
                    gghad.setMachine( 'clic_cdr' )
                    gghad.setDetectorModel( detector.upper() )
                    gghad.setBkgEvtType( 'gghad' )
                    result = job.append( gghad )
                    if not result['OK']:
                        print result['Message']
                        sys.exit(2)

                elif preDefinedSetup in ['CLIC_CDR_1400']:
                    # define input for gghad background overlay
                    gghad = OverlayInput()
                    #gghad.setProdID( 766 )
                    gghad.setEnergy( energy )
                    gghad.setBXOverlay( 60 )
                    gghad.setGGToHadInt( 1.3 )
                    gghad.setNbSigEvtsPerJob( nEvts )
                    gghad.setMachine( 'clic_cdr' )
                    gghad.setDetectorModel( detector.upper() )
                    gghad.setBkgEvtType( 'gghad' )
                    result = job.append( gghad )
                    if not result['OK']:
                        print result['Message']
                        sys.exit(2)
                
                elif preDefinedSetup in ['ILC_DBD_1000']:
                    # define input for gghad background overlay
                    gghad = OverlayInput()
                    #gghad.setProdID( 1767 )
                    gghad.setEnergy( energy )
                    gghad.setBXOverlay( 1 )
                    gghad.setGGToHadInt( 4.1 )
                    gghad.setNbSigEvtsPerJob( nEvts )
                    gghad.setMachine( 'ilc_dbd' )
                    gghad.setDetectorModel( detector )
                    gghad.setBkgEvtType( 'aa_lowpt' )
                    result = job.append( gghad )
                    if not result['OK']:
                        print result['Message']
                        sys.exit(2)
        
                    # define input for pair background overlay
                    pairs = OverlayInput()
                    #pairs.setProdID( 2 )
                    pairs.setEnergy( energy )
                    pairs.setBXOverlay( 1 )
                    pairs.setGGToHadInt( 1. )
                    pairs.setNbSigEvtsPerJob( nEvts )
                    pairs.setMachine( 'ilc_dbd' )
                    pairs.setDetectorModel( detector )
                    pairs.setBkgEvtType( 'eepairs' )
                    result = job.append( pairs )
                    if not result['OK']:
                        print result['Message']
                        sys.exit(2)
                
                else:
                    # define input for gghad background overlay
                    gghad = OverlayInput()
                    gghad.setProdID( 1767 )
                    #gghad.setProdID( 1878 )
                    gghad.setEnergy( energy )
                    gghad.setBXOverlay( 1 )
                    gghad.setGGToHadInt( 4.1 )
                    gghad.setNbSigEvtsPerJob( nEvts )
                    gghad.setMachine( 'ilc_dbd' )
                    gghad.setDetectorModel( detector )
                    gghad.setBkgEvtType( 'aa_lowpt' )
                    result = job.append( gghad )
                    if not result['OK']:
                        print result['Message']
                        sys.exit(2)
        
                    # define input for pair background overlay
                    pairs = OverlayInput()
                    pairs.setProdID( 2 )
                    pairs.setEnergy( energy )
                    pairs.setBXOverlay( 1 )
                    pairs.setGGToHadInt( 1. )
                    pairs.setNbSigEvtsPerJob( nEvts )
                    pairs.setMachine( 'ilc_dbd' )
                    pairs.setDetectorModel( detector )
                    pairs.setBkgEvtType( 'eepairs' )
                    result = job.append( pairs )
                    if not result['OK']:
                        print result['Message']
                        sys.exit(2)
                    
            lcsim = LCSIM()
            lcsim.setVersion( lcsimVer )
            if slicVer:
                lcsim.getInputFromApp( slic )
            #else:
            #    lcsim.setInputFile( inputSlcios )
            lcsim.setEnergy( energy )
            lcsim.setNumberOfEvents( nEvts )
            lcsim.setSteeringFile( xmlFile )
            lcsim.setAliasProperties( aliasFile )
            lcsim.setDetectorModel( detector + '.zip' )
            lcsim.setTrackingStrategy( strategyFile )
            lcsim.setOutputFile( lcsimOutput )
            result = job.append( lcsim )
            if not result['OK']:
                print result['Message']
                sys.exit(2)
        
        if slicPandoraVer:
            slicPandora = SLICPandora()
            slicPandora.setVersion( slicPandoraVer )
            slicPandora.setDetectorModel( slicPandoraDetector )
            slicPandora.setPandoraSettings( settingsFile )
            if lcsimVer:
                slicPandora.getInputFromApp( lcsim )
            #else:
            #    slicPandora.setInputFile( inputSlcios )
            slicPandora.setNumberOfEvents( nEvts )
            slicPandora.setStartFrom( 0 )
            slicPandora.setOutputFile( slicPandoraOutput )
            result = job.append( slicPandora )
            if not result['OK']:
                print result['Message']
                sys.exit(2)
                
        # Marlin for LCFI vertex fitting
        if marlinVer:
            vertexing = Marlin()
            vertexing.setVersion( marlinVer )
            vertexing.setSteeringFile( marlinXml )
            vertexing.setGearFile( gearFile )
            if slicPandoraVer:
                vertexing.getInputFromApp( slicPandora )
            elif lcsimVer:
                vertexing.getInputFromApp( lcsim )
            #else:
            #    vertexing.setInputFile( inputSlcios )
            vertexing.setOutputFile( outputFile + '.slcio' )
            result = job.append( vertexing )
            if not result['OK']:
                print result['Message']
                sys.exit(2)
                
        if lcsimVer and xmlPostPandora:
            lcsimFinalize = LCSIM()
            lcsimFinalize.setVersion( lcsimVer )
            if marlinVer:
                lcsimFinalize.getInputFromApp( vertexing )
            elif slicPandoraVer:
                lcsimFinalize.getInputFromApp( slicPandora )
            elif lcsimVer:
                lcsimFinalize.getInputFromApp( lcsim )
            #else:
            #    lcsimFinalize.setInputFile( inputSlcios )
            lcsimFinalize.setEnergy( energy )
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
        elif marlinVer or slicPandoraVer:
            defaultOutputFile = outputFile + '.slcio'
            if not defaultOutputFile in outputData:
                outputData.append( defaultOutputFile )
        
        job.setOutputSandbox ( outputSandbox )
        job.setInputSandbox ( inputSandbox )
        if inputSlcios:
            job.setInputData( inputSlcios )
        elif inputFile:
            #changed
            job.setInputData( [ inputFile ] )
            #changed
        job.setOutputData ( outputData, storagePath, storageElement )    
        job.setCPUTime( cpuLimit )
        job.setSystemConfig ( systemConfig )
        job.setName ( detector+"_"+process+"_"+jobTitle )
        job.setJobGroup( detector+"_"+process+"_"+jobTitle )
        if destination:
            job.setDestination( destination )
        else:
            job.setBannedSites( bannedSites )
        
        if debug:
            print ''
            print 'Jobs to submit:'
            nTotal = len(lfnlist)*nJobs/mergeSlcioFiles
            if inputFile:
                print '  Number of input files:', len(lfnlist)
                if maxFiles > 0:
                    print '  Maximum input files to use:', maxFiles
                    nTotal = maxFiles*nJobs/mergeSlcioFiles
                if mergeSlcioFiles > 1:
                    print '  Merged input files per job:', mergeSlcioFiles
            if nJobs != 1:
                print '  Jobs per input file:', nJobs
            if nEvts < 0:
                print '  Events per job: all'
            else :
                print '  Events per job:', nEvts
            print '  Total number of jobs:', nTotal
            print '  Maximum CPU time per job:', cpuLimit, 'sec'
            print ''
            
            print 'General parameters:'
            
            print '  Detector model:', detector
            print '  Process name:', process
            print '  Job title:', jobTitle
            if destination:
                print '  Job destination: %s' % ( destination )
            else:
                print '  Banned sites:', bannedSites
            print '  Repository file:', repositoryFile
            print ''
            
            print 'Files:'
            print '  Input sand box:', inputSandbox
            print '  Output sand box:', outputSandbox
            print '  Output data:', outputData
            print '  Output storage path:', storagePath
            print '  Output storage element:', storageElement
            print ''
            
            print 'Steps executed:'
            step = 0
            if slicVer:
                step += 1
                print '  %s) Slic step:'%(step)
                print '    Slic version:', slicVer
                print '    Macro file:', macroFile
                print ''
            
            if lcsimVer:
                step += 1
                print '  %s) LCSim step:'%(step)
                print '    LCSim version:', lcsimVer
                print '    LCSim file:', xmlFile
                print '    Tracking strategies:', strategyFile
                print '    Detector alias file:', aliasFile
                if overlayBX > 0:
                    print '    Number of bunch crossings overlayed:', overlayBX
                    print '    gg->hadron events per bunch crossing:', overlayWeight
                print ''
            
            if slicPandoraVer:
                step += 1
                print '  %s) SlicPandora step:'%(step)
                print '    SlicPandora version:', slicPandoraVer
                mySettingsFile = settingsFile
                if not settingsFile:
                    mySettingsFile = 'default'
                print '    Pandora settings file:', mySettingsFile
                print '    Pandora detector file:', slicPandoraDetector
                print ''
            
            if marlinVer:
                step += 1
                print '  %s) Marlin step:'%(step)
                print '    Marlin version:', marlinVer
                mySettingsFile = settingsFile
                print '    Marlin steering file:', marlinXml
                print '    Gear geometry file:', gearFile
                print ''
            
            if lcsimVer and xmlPostPandora:
                step += 1
                print '  %s) LCSim step:'%(step)
                print '    LCSim version:', lcsimVer
                print '    LCSim file:', xmlPostPandora
                print '    Detector alias file:', aliasFile
                print ''

            answer = raw_input('Proceed and submit job(s)? (Y/N): ')
            if not answer.lower() in ('y', 'yes'):
                sys.exit(2)
                
        if not debug:
            job.dontPromptMe()
        
        if not agentMode:
            #print "submitting"
            job.submit ( dirac )
        else:
            job.submit ( dirac, mode="Agent" )
        
        # switch off prompt after the first job submission
        job.dontPromptMe()
        debug = False

