# Modified BeamCalhist script to create a histogram of hits in the x-y plane of the Beam calorimeter. Only positive
# Slight error as it gives the wrong filename.
# Author Miles Toon , 04/09/15

import os, sys, argparse, os.path
import ROOT
import array

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from ROOT import TFile, TNtuple, TCanvas, TH1F, TAxis, TSystem, TGraph

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

def make_hist(event): # Each detector is a 'collection', the No. of Elements are the hits.
	
	#xcoord = [] # found better way
	#ycoord = []
	BCALhist  = ROOT.TH2D( "BCALhist", "hits on beam calorimeter", 40 , -140, 140, 40, -140 , 140) # Creates the histogram ("name","description", xbins, x low, x high, ybins, y low, y high)
	
	BCAL = event.getCollection("BeamCalHits") # selects the collection to take data from
	nbin = BCAL.getNumberOfElements() # not required, but gets the number of hits in the collection
	for ding in BCAL:					# for all hits in beam cal
		pos = ding.getPosition()		# gets position vector pos[x,y,z]
		if pos[2] > 0:							# if it is at positive z
			BCALhist.Fill(pos[0],pos[1],1)		# fill the histogram with a 1 at the coordinate
			
	return BCALhist # returns the histogram

def draw_hist(BCALhist):
	
	c1 = TCanvas('c1','c1',600,900) # Creates the canvas to draw the histogram to.
	c1.Divide(1,2)		# separates the canvas into two for two plots
	c1.SetGrid()		# Adds grid lines to canvas.

	#hithist.LabelsDeflate("X") 	# Trim the number of bins to match the number of active labels - Took ages to find this, didn't work without.
	c1.cd(1)						# selects first canvas
	BCALhist.Draw("COLZ") 			# Draws the histogram to the canvas, sets draw style.
	BCALhist.SetStats(0)			# removes stats legend
	BCALhist.SetXTitle("X")			# X axis label
	BCALhist.SetYTitle("Y")			# Y axis label
	c1.Update()					# Makes the canvas show the histogram.

	c1.cd(2)						# selects second canvas
	BCALhist.Draw("SURF1") 			# Draws the histogram to the canvas.
	BCALhist.SetStats(0)
	BCALhist.SetXTitle("X")
	BCALhist.SetYTitle("Y")
	c1.Update()					# Makes the canvas show the histogram.
    
	img = ROOT.TImage.Create()				# creates image
	img.FromPad(c1)							# takes it from canvas
	img.WriteImage("BCALsurf+z.png")	# Saves it as png file with this name the the input file directory.

	return c1 # returns the canvas with histograms drawn to it

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
		outputName = os.path.basename(inputpath) + '.png' # change this to edit the tag on the end of the image file
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

			hist = make_hist(event)

			draw_hist(hist)

		reader.close()

	raw_input("press <ENTER> to close")	# Waits for user to press enter so you may view the chart.

	print "\nProcessed " + str(file_counter) + " files."

if __name__=='__main__':
	main()