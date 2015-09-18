# Modified hitCounts script that plots x y z coordinates of the hits on non-beamcal detectors.
# Author Miles Toon , 14/09/15 - revisited

import os, sys, argparse, os.path
import ROOT
import array

from pyLCIO import IOIMPL
from pyLCIO import UTIL
from pyLCIO import EVENT

from ROOT import TFile, TNtuple, TCanvas, TH1F, TAxis, TSystem, TGraph, TLegend

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
	a = TNtuple("a", "a", "x:y:z:cell") # creates ntuple to store the values of x y z
	b = TNtuple("b", "b", "x:y:z:cell") # creates ntuple to store the values of x y z
	c = TNtuple("c", "c", "x:y:z:cell") # creates ntuple to store the values of x y z
	d = TNtuple("d", "d", "x:y:z:cell") # creates ntuple to store the values of x y z
	e = TNtuple("e", "e", "x:y:z:cell") # creates ntuple to store the values of x y z
	f = TNtuple("f", "f", "x:y:z:cell") # creates ntuple to store the values of x y z
	g = TNtuple("g", "g", "x:y:z:cell") # creates ntuple to store the values of x y z
	h = TNtuple("h", "h", "x:y:z:cell") # creates ntuple to store the values of x y z
	i = TNtuple("i", "i", "x:y:z:cell") # creates ntuple to store the values of x y z
	j = TNtuple("j", "j", "x:y:z:cell") # creates ntuple to store the values of x y z
	k = TNtuple("k", "k", "x:y:z:cell") # creates ntuple to store the values of x y z
	l = TNtuple("l", "l", "x:y:z:cell") # creates ntuple to store the values of x y z

	ECALB = event.getCollection("EcalBarrelHits")
	for ding in ECALB:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		a.Fill(x,y,z,cell)

	ECALE = event.getCollection("EcalEndcapHits")
	for ding in ECALE:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		b.Fill(x,y,z,cell)

	HCALB = event.getCollection("HcalBarrelHits")
	for ding in HCALB:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		c.Fill(x,y,z,cell)

	HCALE = event.getCollection("HcalEndcapHits")
	for ding in HCALE:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		d.Fill(x,y,z,cell)

	LUMICAL = event.getCollection("LumiCalHits")
	for ding in LUMICAL:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		e.Fill(x,y,z,cell)

	MUONB = event.getCollection("MuonBarrelHits")
	for ding in MUONB:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		f.Fill(x,y,z,cell)

	MUONE = event.getCollection("MuonEndcapHits")
	for ding in MUONE:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		g.Fill(x,y,z,cell)

	SITB = event.getCollection("SiTrackerBarrelHits")
	for ding in SITB:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		h.Fill(x,y,z,cell)

	SITE = event.getCollection("SiTrackerEndcapHits")
	for ding in SITE:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		i.Fill(x,y,z,cell)

	SITF = event.getCollection("SiTrackerForwardHits")
	for ding in SITF:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		j.Fill(x,y,z,cell)

	SIVB = event.getCollection("SiVertexBarrelHits")
	for ding in SIVB:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		k.Fill(x,y,z,cell)

	SIVE = event.getCollection("SiVertexEndcapHits")
	for ding in SIVE:

		cell = ding.getCellID0()
		pos = ding.getPosition()
		x = pos[0]
		y = pos[1]
		z = pos[2]
		l.Fill(x,y,z,cell)

	return  a, b, c, d, e, f, g, h, i, j, k, l

def make_graph( a, b, c, d, e, f, g, h, i, j, k, l, output ):
	

	c1 = TCanvas("c1","c1", 800, 800) # Creates the canvas to draw the bar chart to.
	c1.SetGrid() # Adds grid lines to canvas.

	leg = TLegend(0.7,0.6,0.95,0.95)
	leg.AddEntry( a, "EcalBarrelHits", "P")
	leg.AddEntry( b, "EcalEndcapHits", "P")
	leg.AddEntry( c, "HcalBarrelHits", "P")
	leg.AddEntry( d, "HcalEndcapHits", "P")
	leg.AddEntry( e, "LumiCalHits", "P")
	leg.AddEntry( f, "MuonBarrelHits", "P")
	leg.AddEntry( g, "MuonEndcapHits", "P")
	leg.AddEntry( h, "SiTrackerBarrelHits", "P")
	leg.AddEntry( i, "SiTrackerEndcapHits", "P")
	leg.AddEntry( j, "SiTrackerForwardHits", "P")
	leg.AddEntry( k, "SiVertexBarrelHits", "P")
	leg.AddEntry( l, "SiVertexEndcapHits", "P")

	#n0 = TNtuple("n0", "n0", "x:y:z") # creates ntuple to store the values of x y z
	#n0.SetMarkerColor(0)
	#n0.Fill(-4500,-4500,-5700)
	#n0.Fill(4500,4500,5700)
	#n0.Draw("x:y:z")

	a.SetMarkerColor(1)
	a.SetMarkerStyle(6)
	a.Draw("cell","","same") 				# Draws the histogram to the canvas.

	b.SetMarkerColor(2)
	b.SetMarkerStyle(6)
	b.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	c.SetMarkerColor(3)
	c.SetMarkerStyle(6)
	c.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	d.SetMarkerColor(4)
	d.SetMarkerStyle(6)
	d.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	e.SetMarkerColor(5)
	e.SetMarkerStyle(6)
	e.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	f.SetMarkerColor(6)
	f.SetMarkerStyle(6)
	f.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	g.SetMarkerColor(7)
	g.SetMarkerStyle(6)
	g.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	h.SetMarkerColor(8)
	h.SetMarkerStyle(6)
	h.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	i.SetMarkerColor(9)
	i.SetMarkerStyle(6)
	i.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	j.SetMarkerColor(30)
	j.SetMarkerStyle(6)
	j.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	k.SetMarkerColor(40)
	k.SetMarkerStyle(6)
	k.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	l.SetMarkerColor(28)
	l.SetMarkerStyle(6)
	l.Draw("cell","", "same") 				# Draws the histogram to the canvas.

	leg.Draw()
	
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
		outputName = os.path.basename(inputpath) + '_posPlotCell.png'
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
			
			a, b, c, d, e, f, g, h, i, j, k, l = get_pos(event)

			make_graph(a, b, c, d, e, f, g, h, i, j, k, l, outputFile)

			
		reader.close()

	raw_input("press <ENTER> to close")	# Waits for user to press enter so you may view the chart.


	print "\nProcessed " + str(file_counter) + " files."

	#print "Outputted to - " + outputFile

if __name__=='__main__':
	main()