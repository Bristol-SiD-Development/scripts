# Modified posPlot script that plots Zenith angle of electrons and positrons. compares ones that left and ones that stayed in detector
# Author Miles Toon , 09/09/15

import os, sys, argparse, os.path
import ROOT
import array

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from ROOT import TFile, TNtuple, TCanvas, TH1F, TAxis, TSystem, TGraph, TGraph2D, TTree, TH3F, TMath, TLegend # not all are used but I'm being safe

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

def get_pos(event): # Each detector is a 'collection', the No. of Elements are the hits.

	i = 0
	j = 0
	n = TH1F("n", "Zenith Angles", 100, 0, 2) # first histogram to be filled with particles below the cut
	m = TH1F("m", "Zenith Angles", 100, 0, 2) # second for above
 	k = 0 # counter for the number of particles below
	mcpart = event.getCollection("MCParticle") # essentially 'opens up' the collection
    
   
	
	for ding in mcpart: # for every entry in the collection - can be called whatever
		mom = ding.getMomentum() # gets the momentum in a 3 vector fro mthe slcio file collection
		left = ding.hasLeftDetector() # checks if the particle has left

		if (ding.getPDG() == 11 or ding.getPDG() == -11) and mom[2]!=0 and left: # condition that only allows electrons or positrons (their pdg id) also, the momenta cant be 0
			
			i+=1

			x = mom[0] # assign a vales from the 3 vector to a variable
			y = mom[1]
			z = mom[2] 
			if z ==0:
				print "weird angle..." # was to show me how many zeros I was getting
			
			t = TMath.Sqrt((x*x)+(y*y)) # calculates transverse momentum using Pythatgoras
			
				
			try: 		# try statement allows to get around division by 0
				theta = TMath.ATan(t / TMath.Abs(z)) # calculate the angle
			except ZeroDivisionError:
			
				theta = 90 # if the z momentum is 0, the angle is 90.

			m.Fill(theta, 1) # fills up the histogram so the value of theta gets 1 extra weight per cycle

		if (ding.getPDG() == 11 or ding.getPDG() == -11) and mom[2]!=0 and left == False: 
			
			j+=1

			x = mom[0] # assign a vales from the 3 vector to a variable
			y = mom[1]
			z = mom[2] 
			if z ==0:
				print "weird angle..." # was to show me how many zeros I was getting
			
			t = TMath.Sqrt((x*x)+(y*y)) # calculates transverse momentum using Pythatgoras
			
				
			try: 		# try statement allows to get around division by 0
				theta = TMath.ATan(t / TMath.Abs(z)) # calculate the angle
			except ZeroDivisionError:
			
				theta = 90 # if the z momentum is 0, the angle is 90.

			n.Fill(theta, 1) # fills the other histogram

	print "number of particles left: ", i, "\nnumber of particles didn't leave: ", j
	return m, n # returns the two histograms

def make_graph(n, m, output): # output is the name for the image that will be saved
	

	c1 = TCanvas() # Creates the canvas to draw the bar chart to.
	c1.SetGrid() # Adds grid lines to canvas.
	c1.cd() 		# selects canvas
	c1.SetLogy(1) 	# sets log scale on y axis
	n.GetXaxis().SetTitle("Zenith Angle (Degrees)")
	n.GetYaxis().SetTitle("Count")

	leg = TLegend(0.6,0.7,0.89,0.89)
	leg.AddEntry(n, "Particles Not Left", "F")
	leg.AddEntry(m, "Particles Have Left", "F")

	n.Draw() 				# Draws the histogram to the canvas.
	n.SetLineColor(12)
	n.SetFillColor(31)
	n.SetStats(0)

	m.Draw("same")			# Draws onto same canvas without replacing
	m.SetStats(0)
	m.SetFillStyle(3344)
	m.SetLineColor(2)
	m.SetFillColor(2)
	
	leg.Draw()

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
		outputName = os.path.basename(inputpath) + '_angle_compare_left.png' # change this entry to tag stuff on the end of the image name
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
			
			m, n = get_pos(event) # assigns the output histograms of the funtion to the variables n and m

			make_graph(n, m, outputFile) 
			
		reader.close()

	raw_input("press <ENTER> to close")	# Waits for user to press enter so you may view the chart.


	print "\nProcessed " + str(file_counter) + " files."

	#print "Outputted to - " + outputFile

if __name__=='__main__':
	main()