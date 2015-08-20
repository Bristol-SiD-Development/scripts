import os, sys, argparse, os.path
import ROOT
import array

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT
from pyLCIO import IOIMPL

from ROOT import TFile, TNtuple

def args_parse():
	# Takes in arguments from the command line, using argparse allows for --help interface.
	currentDir = os.getcwd()
	parser = argparse.ArgumentParser(description='Gets tag data out of LCIO files and outputs then to TNtuple...'
						  ,epilog='In case of questions or problems, contact jt12194@my.bristol.ac.uk')

	parser.add_argument('-i', '--inputDirectory',
						help='Input Directory shall process all files in a directory into one output .root file.',
						default='default')

	parser.add_argument('-f', '--inputFile',
						help='Input file shall just process this file into one .root file.',
						default='default')

	parser.add_argument('-o', '--outputDirectory',
						help='Output directory for the .root output file, default = current directory.',
						default=currentDir)

	parser.add_argument('-n', '--outputName',
						help='output file name, must end with .root, if not given shall be derived from first input file',
						default='default')

	return parser.parse_args()

def event_type(event):
	jetCounter = 0
	mcParticlesSkimmed = event.getCollection("MCParticlesSkimmed")
	for particle in mcParticlesSkimmed:
		if particle.getGeneratorStatus()==3:
			if particle.getPDG() = 1 or particle.getPDG() = -1:
				eventType = "d_tags"
				jetCounter += 1
			if particle.getPDG() = 2 or particle.getPDG() = -2:
				eventType = "u_tags"
				jetCounter += 1
			if particle.getPDG() = 3 or particle.getPDG() = -3:
				eventType = "s_tags"
				jetCounter += 1
			if particle.getPDG() = 4 or particle.getPDG() = -4:
				eventType = "c_tags"
				jetCounter += 1
			if particle.getPDG() = 5 or particle.getPDG() = -5:	
				eventType = "b_tags"
				jetCounter += 1
	if jetCounter > 2:
		print "WARNING!!! WE GOT A MULTI JET"

	return eventType

def get_tag(event):
	# Gets the tagging infro from the input .slcio files, contained within the 'RefinedJets' collection.
	refinedJetCollection = event.getCollection('RefinedJets')
	pidh = UTIL.PIDHandler(refinedJetCollection)
	algo = pidh.getAlgorithmID('lcfiplus')
	ibtag = pidh.getParameterIndex(algo, 'BTag')
	ictag = pidh.getParameterIndex(algo, 'CTag')

	btag = []
	ctag = []

	for jet in refinedJetCollection:
		pid = pidh.getParticleID(jet, algo)
		btag.append(pid.getParameters()[ibtag])
		ctag.append(pid.getParameters()[ictag])

	return btag, ctag

def input_files(inputDirectory, inputFile):
	# Checks the input files and returns list of those to process.
	inputFiles = []
	if inputDirectory != 'default' and os.path.isdir(inputDirectory) and inputFile == 'default':
		print '\nLooking in "' + inputDirectory + '" for input files...'
		fileNum = 0
		for fileName in os.listdir(inputDirectory):
			name, extension = os.path.splitext(fileName)
			if extension not in ['.slcio']:
				print 'ERROR: The file "' + fileName + '" is not valid, skipping!'
			else:
				print fileName + ' - okay'
				inputFiles.append(os.path.join(inputDirectory, fileName))
				fileNum = fileNum + 1 

		if fileNum > 0:
			print "\nA total of " + str(fileNum) + " .slcio files shall be processed"
			return True, inputFiles

		else:
			print 'ERROR: No input files could be found!!!'
			return False, inputFiles

	elif inputFile != 'default' and os.path.exists(inputFile) and inputDirectory == 'default':
		name, extension = os.path.splitext(inputFile)
		if extension not in ['.slcio']:
			print 'The file "' + inputFile + '" can not be used, needs to be a .slcio file. Skipping ...'
			return False, inputFiles
		else:
			print inputFile + ' - okay'
			inputFiles.append(inputFile)
			return True, inputFiles
		
	else:
		print 'ERROR: Can only define either an input directory or an input file. Ensure they exist and are of the .slcio type!!!' 
		return False, inputFiles

def output(outputDirectory, outputName, inputFile):
	# Checks the output path exists and return the .root output file name/path.
	if os.path.isdir(outputDirectory) and outputName == 'default':
		inputpath, extension = os.path.splitext(inputFile)
		outputName = path.basename(inputpath) + '.root'
		print '\nOutput = ' + os.path.join(outputDirectory,outputName)
		return True, os.path.join(outputDirectory,outputName)

	elif os.path.isdir(outputDirectory) and outputName != 'default':
		name, extension = os.path.splitext(outputName)
		if extension not in ['.root']:
			print 'ERROR: Output file must end with .root!!!'
			return False, os.path.join(outputDirectory,outputName)
		else:
			print '\nOutput = ' + os.path.join(outputDirectory,outputName)
			return True, os.path.join(outputDirectory,outputName)

	else:
		print 'ERROR: Output directory does not exist!!!'
		print outputDirectory
		return False, os.path.join(outputDirectory,outputName)

def main():
	# main
	args = args_parse()

	if not args:
		print 'Invalid Arguments'
		sys.exit(1)

	# Setup the input files list, checks they have the .slcio extension...
	input_check, inputFiles = input_files(args.inputDirectory, args.inputFile)
	if not input_check:
		sys.exit(1)

	output_check, outputFile = output(args.outputDirectory, args.outputName, inputFiles[0])
	if not output_check:
		sys.exit(1)

	f = ROOT.TFile(outputFile, "RECREATE")
	f.cd()

	# tntuple = ROOT.TNtuple("tags","tags","batg:ctag")

	dtuple = ROOT.TNtuple("d_tags", "d_tags", "btag:ctag")
	utuple = ROOT.TNtuple("u_tags", "u_tags", "btag:ctag")
	stuple = ROOT.TNtuple("s_tags", "s_tags", "btag:ctag")
	ctuple = ROOT.TNtuple("c_tags", "c_tags", "btag:ctag")
	btuple = ROOT.TNtuple("b_tags", "b_tags", "btag:ctag")

	list1 = []
	list2 = []

	dCount = uCount = sCount = cCount = bCount = 0
	file_counter = 0

	print "\nProcessing File->"

	for filename in inputFiles:
		file_counter += 1
		print str(file_counter) + "..."

		reader = IOIMPL.LCFactory.getInstance().createLCReader()
		reader.open(filename)

		for event in reader:
			tag_b, tag_c = get_tag(event)
			list1 = [tag_b[0], tag_c[0]]
			list2 = [tag_b[1], tag_c[1]]

			if event_type(event) = "d_tags":
				dCount += 1
				dtuple.Fill(array.array("f", list1))
				dtuple.Fill(array.array("f", list2))
			if event_type(event) = "u_tags":
				uCount += 1
				utuple.Fill(array.array("f", list1))
				utuple.Fill(array.array("f", list2))
			if event_type(event) = "s_tags":
				sCount += 1
				stuple.Fill(array.array("f", list1))
				stuple.Fill(array.array("f", list2))
			if event_type(event) = "c_tags":
				cCount += 1
				ctuple.Fill(array.array("f", list1))
				ctuple.Fill(array.array("f", list2))
			if event_type(event) = "b_tags":
				bCount += 1
				btuple.Fill(array.array("f", list1))
				btuple.Fill(array.array("f", list2))

		reader.close()

	f.cd()
	tntuple.Write()
	print "\nProcessed " + str(file_counter) " files."
	print "Containing a total of..."
	print str(dCount) + " ddbar events."
	print str(uCount) + " uubar events."
	print str(sCount) + " ssbar events."
	print str(cCount) + " ccbar events."
	print str(bCount) + " bbbar events."
	print "Outputted to - " + outputFile

if __name__=='__main__':
	main()