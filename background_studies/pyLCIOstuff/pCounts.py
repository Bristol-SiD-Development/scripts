# Modified pyLCIO_e script that creates a histogram showing number of each particle.
# Author Miles Toon , 03/09/15

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

def p_count(event): # Each detector is a 'collection', the No. of Elements are the hits.
	
	mcpart = event.getCollection("MCParticle") 

	a = 0 # e+
	b = 0 # e-
	c = 0 # gamma
	d = 0 # n
	e = 0 # p
	f = 0 # pi0
	g = 0 # pi+
	h = 0 # pi-
	i = 0 # mu+

	for particle in mcpart: # loops through all entries in the collection

		if particle.getPDG()==-11: # each one of these counts up every time it spots a particle
			a+=1
		if particle.getPDG()==-11:
			b+=1
		if particle.getPDG()==22:
			c+=1
		if particle.getPDG()==2112:
			d+=1
		if particle.getPDG()==2212:
			e+=1
		if particle.getPDG()==111:
			f+=1
		if particle.getPDG()==211:
			g+=1
		if particle.getPDG()==-211:
			h+=1
		if particle.getPDG()==-13:
			i+=1


	return a, b, c, d, e, f, g, h, i

def make_graph( a, b, c, d, e, f, g, h, i, output ):
	

	c1 = TCanvas() # Creates the canvas to draw the bar chart to.
	c1.SetGrid() # Adds grid lines to canvas.
	c1.SetLogy(1)

	phist  = ROOT.TH1F( "phist", "particle count", 9, 0, 0) # Creates the histogram with 9 bins.
	phist.SetFillColor(46) 			# Makes bars red


	phist.Fill('e+', a) # fills each bin/bar with the variable
	phist.Fill('e-', b)
	phist.Fill('gamma', c)
	phist.Fill('n', d)
	phist.Fill('p', e)
	phist.Fill('pi0', f)
	phist.Fill('pi+', g)
	phist.Fill('pi-', h)
	phist.Fill('mu+', i)



	phist.LabelsDeflate("X") 	# Trim the number of bins to match the number of active labels - Took ages to find this, didn't work without.
	phist.Draw("BAR1") 				# Draws the histogram to the canvas.
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
		outputName = os.path.basename(inputpath) + '_pcount.png' # cahnge this to edit the tag on the end of saved image files
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
			
			a, b, c, d, e, f, g, h, i = p_count(event)	# Calls function to get the values for variables.

			print a, b, c, d, e, f, g, h, i				# Check to see if you're outputting correctly.

			c1 = make_graph( a, b, c, d, e, f, g, h, i, outputFile )	# Makes your plot.



		reader.close()

	raw_input("press <ENTER> to close")	# Waits for user to press enter so you may view the chart.

	print "\nProcessed " + str(file_counter) + " files."

	#print "Outputted to - " + outputFile

if __name__=='__main__':
	main()