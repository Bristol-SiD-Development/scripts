# THIS SCRIPT USES THE NEW API
# author: jt12194@my.bristol.ac.uk based on script by jan.strube@cern.ch
from DIRAC.Core.Base import Script
Script.initialize()
from ILCDIRAC.Interfaces.API.DiracILC import DiracILC
from ILCDIRAC.Interfaces.API.NewInterface.UserJob import UserJob
from ILCDIRAC.Interfaces.API.NewInterface.Applications import SLIC, LCSIM, SLICPandora, Marlin, OverlayInput
from DIRAC.Resources.Catalog.FileCatalogClient import FileCatalogClient
import sys
import os.path
import os.path as path
import re
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description='Handle the full SiD reconstruction chain (including flavourtagging)'
						  , epilog='In case of questions or problems, please contact the author.')

	parser.add_argument('stdhepInput', help= 'LFN path to the input stdhep file')

	#parser.add_argument('--events'
	#                  , help='The first argument to this option is the total number of events you wish to run from the input file. The second argument (optional) is the number of events in each output file. If one of the arguments is < 0, this option is ignored. By default the input files are not split.'
	#                  , type=int
	#                  , default=[-1, -1]
	#                  , nargs=2
	#                  , metavar=('nEvents_Source', 'nEvents_per_chunk') )

	parser.add_argument('-r' ,'--events'
					  , help='Total number of events to use from input file'
					  , default = -1)

	parser.add_argument('-s','--split'
					  , help='The number of events to output into seperate output files (must be a value less than --runs). Default not split'
					  , default = -1)

	parser.add_argument('-d', '--detector'
					  , help='Name of the detector model (default=%(default)s)'
					  , default='sidloi3')

	parser.add_argument('-m', '--macFile'
					  , help='macro file to pass to SLIC (default=%(default)s)'
					  , default='steeringFiles/defaultILCCrossingAngle.mac') # NEED TO GET THIS FILE!!!!!

	parser.add_argument('--SE'
					  , help='Name of the Storage Element'
					  , choices=['CERN-SRM', 'RAL-SRM', 'SLAC-SRM', 'PNNL-SRM']
					  , default='CERN-SRM')

	parser.add_argument('--site'
					  , help='Force the job to a given site (default=allow any site)')

	parser.add_argument('--dontPromptMe'
					  , help='do not wait for user to confirm first job'
					  , action='store_true')

	parser.add_argument('-o', '--outputPath'
					  , help='Path in the file catalog where the files should go, e.g. "SID_DBD/ILC1000/optimization/clic_sid_cdr"'
					  , default='default')

	return parser.parse_args()

def check_events_arguments(events, split_size):
	checkEvents = events > 0 
	checkSplit = split_size > 0
	if not checkEvents:
		print 'Error: The number of events must be specified with (--events) when calling script'
		return False
	elif checkEvents and checkSplit and split_size > events:
		print 'Error: The total number of events (--runs) must be greater than the output size (--split)'
		return False
	elif checkEvents and not checkSplit:
		print 'Total number of events to run = ', events, '. NO SPLIT'
		return True
	elif checkEvents and checkSplit and events > split_size:
		print 'Total number of events to run = ', events, '. SPLIT, into files of size = ', split_size, ' events.'
		return True

def check_input_LFN(input_lfn):
	lfn, extension = os.path.splitext(input_lfn) 
	if extension not in ['.stdhep']:
		print 'Error: Do not understand the extension', extension
		return False, input_lfn 
	else:
		print 'Input LFN = ', input_lfn
		return True, input_lfn

#def setup_steering_dict():
#	steering_files = {'xmlPrePandora':'steeringFiles/sid_dbd_prePandora_noOverlay.xml',
#					  'xmlPostPandora':'steeringFiles/sid_dbd_postPandora.xml',
#					  'trackingStrategies':'steeringFiles/sidloi3_trackingStrategies_default.xml',
#					  'lcsimGeometry':'geometryFiles/sidloi3.zip',
#					  'pandoraSettings':'steeringFiles/sid_dbd_pandoraSettings.xml',
#					  'marlinVertexing':'steeringFiles/sid_dbd_vertexing.xml',
#					  'marlinGearFile':'steeringFiles/sidloi3.gear'}
#	return steering_files

def setup_output_dict(input_lfn, detector, fileNumber, outputPath):
	lfn, extension = os.path.splitext(input_lfn)
	baseName = path.basename(lfn) + '_' + detector + '_' + str(fileNumber) + ".slcio"
	defaultOutput = path.basename(lfn) + '_' + detector
	print "    Output BaseName = ", baseName
	output_files = {'slicOutput':baseName.replace('.slcio', '_slic.slcio'),
					'prePandoraOutput':baseName.replace('.slcio', '_lcsimDigi.slcio'),
					'pandoraOutput':baseName.replace('.slcio', '_pandora.slcio'),
					'vertexingOutput':baseName.replace('.slcio', '_vertexing.slcio'),
					'lcsimRecOutput':baseName.replace('.slcio', '_Rec.slcio'),
					'lcsimDstOutput':baseName.replace('.slcio', '_DST.slcio')}
	if outputPath=='default':
		output_files['diracOutput']=defaultOutput
		print "Default output path = " + output_files['diracOutput']
	else:
		output_files['diracOutput']=outputPath
		print "User defined output path = " + output_files['diracOutput']
	return output_files

def setup_repository_name(input_lfn, detector):
	lfn, extension = os.path.splitext(input_lfn) 
	return path.basename(lfn) + '_' + detector + '_repository.cfg'

def setup_sandboxes(macFile): # CAN ADD THINGS IN HERE IF THINGS DONT SEEM TO BE WORKING,
	inputSandbox = ["LFN:/ilc/user/j/jtingey/pandoraSettings/pandoraSettings.xml"]
	outputSandbox = ['*.log', '*.xml', '*.lcsim', '*.slcio', '*.mac'] # WOULD BE COOL TO HAVE THIS DEPENDANT ON INPUT
	if macFile != 'defaultIlcCrossingAngle.mac':
		inputSandbox.append(macFile)
	return inputSandbox, outputSandbox

def main():
	# Take the input arguments from the argument parser, and check they exist...
	args = parse_args()
	if not args:
		print 'Invalid Arguments'
		sys.exit(1)

	# Setup the steering files dictionary this is hardcoded at the moment and should be improved...
	# steeringFiles = setup_steering_dict

	# Check the --runs and --split arguments to make sure they are compatible, if not exit... 
	if not check_events_arguments(args.events, args.split):
		sys.exit(1)

	# Check the input LFN given by user, it needs to have .stdhep extension and should not have LFN: at the beginning...
	lfn_check, lfn = check_input_LFN(args.stdhepInput)
	if not lfn_check:
		sys.exit(1)

	# Call when you begin ILC-DIRAC jobs, the true indicates a repository file is included...
	dirac = DiracILC(True, setup_repository_name(args.stdhepInput, args.detector))

	inputSandbox, outputSandbox = setup_sandboxes(args.macFile)

	if args.split < 0:
		nInputEvents = int(args.events)
		nOutputEvents = int(args.events)
	if args.split > 0:
		nInputEvents = int(args.events)
		nOutputEvents = int(args.split)

	for startEvent in range(0, nInputEvents, nOutputEvents):

################## Job Initialise ########################################		
		job = UserJob()
		job.setName(path.basename(args.stdhepInput))
		job.setJobGroup('JobGroup')
		job.setInputSandbox(inputSandbox)
		fileNumber = startEvent/nOutputEvents
		print "Job ", fileNumber

		outputFiles = setup_output_dict(args.stdhepInput, args.detector, fileNumber, args.outputPath)
		slicOutput=outputFiles['slicOutput']
		prePandoraOutput=outputFiles['prePandoraOutput']
		pandoraOutput=outputFiles['pandoraOutput']
		vertexingOutput=outputFiles['vertexingOutput']
		lcsimRecOutput=outputFiles['lcsimRecOutput']
		lcsimDstOutput=outputFiles['lcsimDstOutput']
		diracOutput=outputFiles['diracOutput']

################## SLIC ##################################################
		slic = SLIC()
		slic.setVersion('v3r0p3')
		slic.setSteeringFile(args.macFile)
		# slic.setInputFile(lfn)
		slic.setOutputFile(slicOutput)
		slic.setDetectorModel(args.detector)
		slic.setNumberOfEvents(nOutputEvents)
		slic.setStartFrom(startEvent)
		#print slic.listAttributes()
		result = job.append(slic)
		if not result['OK']:
			# job.append will return an error message if your application object is not properly initialised
			print result['Message']
			sys.exit(2)

################## lcsim (digitization and tracking) #####################
		lcsim = LCSIM()
		lcsim.setVersion('2.5')
		lcsim.setSteeringFile('steeringFiles/sid_dbd_prePandora_noOverlay.xml')
		lcsim.getInputFromApp(slic)
		lcsim.setTrackingStrategy('steeringFiles/sidloi3_trackingStrategies_default.xml')
		# lcsim.setAliasProperties('alias.properties')
		lcsim.setDetectorModel('geometryFiles/sidloi3.zip')
		lcsim.setOutputFile(prePandoraOutput)
		lcsim.setNumberOfEvents(nOutputEvents)
		#print lcsim.listAttributes()
		result = job.append(lcsim)
		if not result['OK']:
			print result['Message']
			sys.exit(2)

################## slicPandora ###########################################
		slicPandora = SLICPandora()
		slicPandora.setVersion('ILC_DBD')
		slicPandora.setDetectorModel(args.detector)
		slicPandora.getInputFromApp(lcsim)
		slicPandora.setOutputFile(pandoraOutput)
		slicPandora.setPandoraSettings('pandoraSettings.xml')
		slicPandora.setNumberOfEvents(nOutputEvents)
		#print slicPandora.listAttributes()
		result = job.append(slicPandora)
		if not result['OK']:
			print result['Message']
			sys.exit(2)

################## Marlin (Vertexing) ####################################
		vertexing = Marlin()
		vertexing.setVersion('0116')
		vertexing.setSteeringFile('steeringFiles/sid_dbd_vertexing.xml')
		vertexing.setGearFile('steeringFiles/sidloi3.gear')
		vertexing.getInputFromApp(slicPandora)
		vertexing.setOutputFile(vertexingOutput)
		vertexing.setNumberOfEvents(nOutputEvents)
		#print vertexing.listAttributes()
		result = job.append(vertexing)
		if not result['OK']:
			print result['Message']
			sys.exit(2)

################## lcsim (DST production) ################################
		lcsimDst = LCSIM()
		lcsimDst.setVersion('2.5')
		lcsimDst.setSteeringFile('steeringFiles/sid_dbd_postPandora.xml')
		lcsimDst.getInputFromApp(vertexing)
		lcsimDst.setNumberOfEvents(nOutputEvents)
		# lcsimDst.setAliasProperties('alias.properties')
		lcsimDst.setDetectorModel('geometryFiles/sidloi3.zip')
		lcsimDst.setOutputRecFile(lcsimRecOutput)
		lcsimDst.setOutputDstFile(lcsimDstOutput)
		#print lcsimDst.listAttributes()
		result = job.append(lcsimDst)
		if not result['OK']:
			print result['Message']
			sys.exit(2)

################## Job Finalise ##########################################
		job.setBannedSites(['LCG.IN2P3-CC.fr', 'LCG.RAL-LCG2.uk', 'LCG.DESY-HH.de', 'LCG.DESYZN.de', 'LCG.KEK.jp'])
		job.setCPUTime(50000)
		job.setPlatform('x86_64-slc5-gcc43-opt')
		job.setOutputData(lcsimDstOutput, diracOutput, args.SE)
		job.setOutputSandbox(outputSandbox)
		job.setInputData(lfn)
		if args.dontPromptMe:
			job.dontPromptMe()
		job.submit()


	return 0;

if __name__=='__main__':
	main()