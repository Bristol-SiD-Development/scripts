# Modified pyLCIO_e script for use in determining hits per each sub-detector.
# Creates a bar chart that saves to input file folder. Slight error as it gives the wrong filename.
# Author Miles Toon , 02/09/15

import os, sys, argparse, os.path
import ROOT
import array

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT
from pyLCIO import IOIMPL

from ROOT import TFile, TNtuple, TCanvas, TH1F, TAxis, TSystem

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

def hit_count(event): # Each detector is a 'collection', the No. of Elements are the hits.
	
	BCAL = event.getCollection("BeamCalHits") 
	a = BCAL.getNumberOfElements()

	ECALB = event.getCollection("EcalBarrelHits")
	b = ECALB.getNumberOfElements()

	ECALE = event.getCollection("EcalEndcapHits")
	c = ECALE.getNumberOfElements()

	HCALB = event.getCollection("HcalBarrelHits")
	d = HCALB.getNumberOfElements()

	HCALE = event.getCollection("HcalEndcapHits")
	e = HCALE.getNumberOfElements()

	LUMICAL = event.getCollection("LumiCalHits")
	f = LUMICAL.getNumberOfElements()

	MUONB = event.getCollection("MuonBarrelHits")
	g = MUONB.getNumberOfElements()

	MUONE = event.getCollection("MuonEndcapHits")
	h = MUONE.getNumberOfElements()

	SITB = event.getCollection("SiTrackerBarrelHits")
	i = SITB.getNumberOfElements()

	SITE = event.getCollection("SiTrackerEndcapHits")
	j = SITE.getNumberOfElements()

	SITF = event.getCollection("SiTrackerForwardHits")
	k = SITF.getNumberOfElements()

	SIVB = event.getCollection("SiVertexBarrelHits")
	l = SIVB.getNumberOfElements()

	SIVE = event.getCollection("SiVertexEndcapHits")
	m = SIVE.getNumberOfElements()

	return a, b, c, d, e, f, g, h, i, j, k, l, m

def make_graph( a, b, c, d, e, f, g, h, i, j, k, l, m, output ):
	

	c1 = TCanvas() # Creates the canvas to draw the bar chart to.
	c1.SetGrid() # Adds grid lines to canvas.
	c1.SetLogy(1)

	hithist  = ROOT.TH1F( "hithist", "hits per sub detector", 13, 0, 0) # Creates the histogram with 13 bins.
	hithist.SetFillColor(38) 			# Makes bars blue
	hithist.Fill('BeamCalHits', a) 		
	hithist.Fill('EcalBarrelHits', b) 	# Allows to add string to bin label (not numbers) 
	hithist.Fill('EcalEndcapHits', c)	# Second value is the weight (number of hits)
	hithist.Fill('HcalBarrelHits', d)
	hithist.Fill('HcalEndcapHits', e)
	hithist.Fill('LumiCalHits', f)
	hithist.Fill('MuonBarrelHits', g)
	hithist.Fill('MuonEndcapHits', h)
	hithist.Fill('SiTrackerBarrelHits', i)
	hithist.Fill('SiTrackerEndcapHits', j)
	hithist.Fill('SiTrackerForwardHits', k)
	hithist.Fill('SiVertexBarrelHits', l)
	hithist.Fill('SiVertexEndcapHits', m)

	hithist.LabelsDeflate("X") 	# Trim the number of bins to match the number of active labels - Took ages to find this, didn't work without.
	hithist.Draw() 				# Draws the histogram to the canvas.
	c1.Update()					# Makes the canvas show the histogram.
    
	img = ROOT.TImage.Create()				# creates image
	img.FromPad(c1)							# takes it from canvas
	img.WriteImage(output)	# Saves it to png file with this name in input file directory.

	return c1

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
		outputName = os.path.basename(inputpath) + '_hitcount.png'
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

	file_counter = 0
	event_counter = 0

	print "\nProcessing File->"

	for filename in inputFiles:
		file_counter += 1
		print str(file_counter) + "..."

		reader = IOIMPL.LCFactory.getInstance().createLCReader()
		reader.open(filename)

		output_check, outputFile = output(args.outputDirectory, args.outputName, inputFiles[0])
		if not output_check:
			sys.exit(1)

		for event in reader:
			
			a, b, c, d, e, f, g, h, i, j, k, l, m = hit_count(event)	# Calls function to get the values for variables.

			print a, b, c, d, e, f, g, h, i, j, k, l, m 				# Check to see if you're outputting correctly.

			c1 = make_graph( a, b, c, d, e, f, g, h, i, j, k, l, m, outputFile )	# Makes your plot.



		reader.close()

	raw_input("press <ENTER> to close")	# Waits for user to press enter so you may view the chart.

	print "\nProcessed " + str(file_counter) + " files."

	#print "Outputted to - " + outputFile

if __name__=='__main__':
	main()