import os, sys, argparse, os.path
import ROOT
import array

from ROOT import *

def parse_args():
	currentDir = os.getcwd()
	parser = argparse.ArgumentParser(description='Processes .root file containing tag data from pyLCIO_tag.py'
						  ,epilog='In case of questions or problems, contact jt12194@my.bristol.ac.uk')

	parser.add_argument('inputFile', help='Input .root file, produced from pyLCIO_tag.py')

	parser.add_argument('-o', '--outputDirectory',
						help='Output directory for plots to be saved to, default = current directory.',
						default=currentDir)

	parser.add_argument('-n', '--outputName',
						help='BaseName for output plots',
						default='default')

	parser.add_argument('-hist', '--basicHistograms',
						help='Include to produce basic histograms for btag and ctag data.',
						action='store_true', default = False)

	parser.add_argument('-back', '--backgroundPlots',
						help='Include to produce Fake rate vs efficiency plots for both btag and ctag data.',
						action='store_true', default = False)

	parser.add_argument('-pur', '--purityPlot',
						help='Include to produce purity plot comparing btag and ctag data.',
						action='store_true', default = False)

	return parser.parse_args()

def input_output(inputFile, outputDirectory, outputName):
	# Checks input file and returns the path/names of the output plots.
	outputPlots = []
	inputName, inputExtension = os.path.splitext(inputFile)
	if not os.path.exists(inputFile) or inputExtension not in [".root"]:
		print "ERROR: Input file '" + inputFile + "' is not valid!"
		return False, outputPlots
	elif os.path.isdir(outputDirectory) and outputName == "default":
		outputPlots.append(os.path.join(outputDirectory, "btag.png"))
		outputPlots.append(os.path.join(outputDirectory, "ctag.png"))
		outputPlots.append(os.path.join(outputDirectory, "btagBack.png"))
		outputPlots.append(os.path.join(outputDirectory, "ctagBack.png"))
		outputPlots.append(os.path.join(outputDirectory, "purity.png"))
		return True, outputPlots
	elif os.path.isdir(outputDirectory) and outputName != "default":
		outputPlots.append(os.path.join(outputDirectory, outputName + "_btag.png"))
		outputPlots.append(os.path.join(outputDirectory, outputName + "_ctag.png"))
		outputPlots.append(os.path.join(outputDirectory, outputName + "_btagBack.png"))
		outputPlots.append(os.path.join(outputDirectory, outputName + "_ctagBack.png"))
		outputPlots.append(os.path.join(outputDirectory, outputName + "_purity.png"))
		return True, outputPlots
	else:
		print "ERROR: Output path not valid!"
		return False, outputPlots

def draw_histograms(hists):
	# Draws the basic histograms and saves to folder.
	c = TCanvas()
	c.SetLogy()

	hists[0].Draw("same")
	hists[2].Draw("same")
	hists[4].Draw("same")

	input1 = raw_input()


#def draw_backgroundPlots():
	# Draws plots for both btag and ctag data of fakes rates vs efficiency, and saves to folder.

#def draw_purityPlot():
	# Draws purity plot and saves to folder.

def check_input(f):
	# Checks the input ntuple. Need to contain structure of pyLCIO_tag.py output.
	# Checks to see each leaf has content > 0.
	# Outputs number of each type of decay.
	tagData = ["d_tags", "u_tags", "s_tags", "c_tags", "b_tags"]
	goodCount = 0
	for eventType in tagData:
		if f.Get(eventType) and f.Get(eventType).GetEntries():
			goodCount += 1
			print eventType + "->" + str(f.Get(eventType).GetEntries())
			if goodCount==5: return True
		else:
			print "ERROR: Input file must be produced from pyLCIO_tag.py and have entries in all decay paths!"
			return False

def histsBranchCorrected(f):
	# Creates the base histograms, to be used by the draw functions.
	# Corrects the data so the branching ratios's are correct.
	histTypes=["d_tags","u_tags","s_tags","c_tags","b_tags"]
	histemp = []
	ratios = [0.2263,0.1596,0.2263,0.1719,0.2160]
	totalEvents = 0
	for hist in histTypes:
		histTemp1 = ROOT.TH1F(hist + "_btag",hist + "_btag",100,0,1)
		histTemp2 = ROOT.TH1F(hist + "_ctag",hist + "_ctag",100,0,1)
		f.Get(hist).Project(hist + "_btag", "btag")
		f.Get(hist).Project(hist + "_ctag", "ctag")
		totalEvents += histTemp1.GetEntries()
		histemp.append(histTemp1)
		histemp.append(histTemp2)

	print "Total Events -> "+ str(totalEvents)

	index2 = 0
	for index in range(0,10,2):
		entries = histemp[index].GetEntries()
		histemp[index].Scale(ratios[index2]/(entries/totalEvents))
		histemp[index+1].Scale(ratios[index2]/(entries/totalEvents))
		index2 += 1

	uds_btag = histemp[0] + histemp[2] + histemp[4]
	uds_ctag = histemp[1] + histemp[3] + histemp[5]
	hists = [histemp[8],histemp[9],histemp[6],histemp[7],uds_btag,uds_ctag]
	return hists

def main():
	# Parse command line arguments into main, via argparse.
	args = parse_args()
	# Check to see if args exist if not exit
	if not args:
		print 'Invalid Arguments'
		sys.exit(1)
	# Check the input and output paths, if they dont exist exit. Also produce the output plot names.
	IOCheck, outputPlots = input_output(args.inputFile, args.outputDirectory, args.outputName)
	if not IOCheck:
		sys.exit(1)
	# Open the input file.
	f = ROOT.TFile(args.inputFile, "READ")
	# Check the input file to ensure it is of the correct structure and contains data needed.
	if not check_input(f):
		sys.exit(1)

	hists = histsBranchCorrected(f)

	draw_histograms(hists)

if __name__=='__main__':
	main()