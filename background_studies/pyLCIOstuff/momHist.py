# Modified hitCounts script that creates a histogram of all the transverse momenta.
# Author Miles Toon , 07/09/15

import os, sys, argparse, os.path
import ROOT
import array

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from ROOT import TFile, TNtuple, TCanvas, TH1F, TAxis, TSystem, TGraph, TGraph2D, TTree, TH3F, TMath

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

def get_mom(event): # Each detector is a 'collection', the No. of Elements are the hits.

	n = TH1F("n", "Transverse Momenta", 100, 0, 2) # creates 1d histogram
	mcpart = event.getCollection("MCParticle") 
	for ding in mcpart: 							# for every entry in the collection
		if ding.getPDG() == 11 or ding.getPDG() == -11: # only if it is electron or positron
			mom = ding.getMomentum()

			x = mom[0] # assigns value to variable
			y = mom[1]
			
			t = TMath.Sqrt((x*x)+(y*y)) # calculates the transverse momentum using Pythagoras
			n.Fill(t, 1) # fills the histogram
			
	return n

def make_graph(n, output):
	

	c1 = TCanvas() # Creates the canvas to draw the bar chart to.
	c1.SetGrid() # Adds grid lines to canvas.
	c1.cd()
	c1.SetLogy(1)

	n.Draw("BAR1") 				# Draws the histogram to the canvas.
	n.SetFillColor(8)
	#htemp.getXaxis().SetLimits(-100, 100)
	#htemp.getYaxis().SetLimits(-100, 100)
	c1.Update()					# Makes the canvas show the histogram.
    
	img = ROOT.TImage.Create()				# creates image
	img.FromPad(c1)							# takes it from canvas
	img.WriteImage(output)	# Saves it to png file with this name in input file directory.

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
		outputName = os.path.basename(inputpath) + '_mom.png'
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

		output_check, outputFile = output(args.outputDirectory, args.outputName, filename)
		if not output_check:
			sys.exit(1)

		for event in reader:
			
			n = get_mom(event)

			make_graph(n, outputFile)
			
		reader.close()

	raw_input("press <ENTER> to close")	# Waits for user to press enter so you may view the chart.

	print "\nProcessed " + str(file_counter) + " files."

if __name__=='__main__':
	main()