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

	parser.add_argument('-bins', '--numberOfBins',
						help='The number of bins in the histograms.',
						default=100)

	return parser.parse_args()

def input_output(inputFile, outputDirectory, outputName):
	# Checks input file and returns the path/names of the output plots.
	outputPlots = []
	plotName = ["btag.png","ctag.png","btagback.png","ctagback.png","purity.png"]
	inputName, inputExtension = os.path.splitext(inputFile)
	if not os.path.exists(inputFile) or inputExtension not in [".root"]:
		print "ERROR: Input file '" + inputFile + "' is not valid!"
		return False, outputPlots
	elif os.path.isdir(outputDirectory) and outputName == "default":
		for name in plotName:
			outputPlots.append(os.path.join(outputDirectory, name))
			print os.path.join(outputDirectory, name)
		return True, outputPlots
	elif os.path.isdir(outputDirectory) and outputName != "default":
		for name in plotName:
			outputPlots.append(os.path.join(outputDirectory, outputName + name))
			print os.path.join(outputDirectory, outputName + name)
		return True, outputPlots
	else:
		print "ERROR: Output path not valid!"
		return False, outputPlots

def check_input(f):
	# Checks the input ntuple. Need to contain structure of pyLCIO_tag.py output.
	# Checks to see each leaf has content > 0.
	# Outputs number of each type of decay.
	tagData = ["d_tags", "u_tags", "s_tags", "c_tags", "b_tags"]
	goodCount = 0
	totalEvents = 0
	for eventType in tagData:
		if f.Get(eventType) and f.Get(eventType).GetEntries():
			goodCount += 1
			totalEvents += f.Get(eventType).GetEntries()
			print eventType + "->" + str(f.Get(eventType).GetEntries())
			if goodCount==5:
				print "Total Events -> "+ str(totalEvents)
				return True, totalEvents
		else:
			print "ERROR: Input file must be produced from pyLCIO_tag.py and have entries in all decay paths!"
			return False, totalEvents

def histsBranchCorrected(f, totalEvents, bins):
	# Creates the base histograms, to be used by the draw functions.
	# Corrects the data so the branching ratios's are correct.
	# Add the u,d,s hists together to make total uds hist.
	# hists is returned with structure ->
		# hists[0] = d_tags_btag
		# hists[1] = d_tags_ctag
		# hists[2] = u_tags_btag
		# hists[3] = u_tags_ctag
		# hists[4] = s_tags_btag
		# hists[5] = s_tags_ctag
		# hists[6] = c_tags_btag
		# hists[7] = c_tags_ctag
		# hists[8] = b_tags_btag
		# hists[9] = b_tags_ctag
		# hists[10] = uds_tags_btag
		# hists[11] = uds_tags_ctag
		  
	histTypes=["d_tags","u_tags","s_tags","c_tags","b_tags"]
	ratios = [0.2263,0.1596,0.2263,0.1719,0.2160]
	hists = []
	index = 0
	for hist in histTypes:
		histTemp1 = ROOT.TH1F(hist + "_btag",hist + "_btag", bins,0,1)
		histTemp2 = ROOT.TH1F(hist + "_ctag",hist + "_ctag", bins,0,1)
		f.Get(hist).Project(hist + "_btag", "btag")
		f.Get(hist).Project(hist + "_ctag", "ctag")
		entries = histTemp1.GetEntries()
		histTemp1.Scale(ratios[index]/(entries/totalEvents))
		histTemp2.Scale(ratios[index]/(entries/totalEvents))
		hists.append(histTemp1)
		hists.append(histTemp2)
		index += 1

	hists.append(ROOT.TH1F("uds_btag","uds_btag", bins,0,1))
	hists.append(ROOT.TH1F("uds_ctag","uds_ctag", bins,0,1))
	hists[10].Add(hists[0],hists[2])
	hists[10].Add(hists[10],hists[4])
	hists[11].Add(hists[1],hists[3])
	hists[11].Add(hists[10],hists[5])
	return hists

def draw_histograms(hist1,hist2,hist3,output):
	# Draws the basic histograms, given the appropriate hists by main().
	c = TCanvas()
	c.SetLogy()
	hist1.SetLineColor(kBlue)
	hist2.SetLineColor(kGreen)
	hist3.SetLineColor(kRed)
	hist3.SetMinimum(10)
	hist3.Draw("same")
	hist2.Draw("same")
	hist1.Draw("same")
	img = ROOT.TImage.Create()
	img.FromPad(c)
	img.WriteImage(output)
	del c, hist1, hist2, hist3, img

def draw_backgroundPlots(hist1, hist2, hist3, bins, output):
	# Draws plots for both btag and ctag data of fakes rates vs efficiency, and saves to folder.
	efficiency = []
	heavyBack = []
	udsBack = []
	binCont1 = 0
	binCont2 = 0 
	binCont3 = 0
	i1 = bins
	while i1 > 0:
		binCont1 = binCont1 + hist1.GetBinContent(i1)
		binCont2 = binCont2 + hist2.GetBinContent(i1)
		binCont3 = binCont3 + hist3.GetBinContent(i1)
		efficiency.append(binCont1)
		heavyBack.append(binCont2)
		udsBack.append(binCont3)
		i1 = i1 - 1

	i2 = 0
	while i2 < bins:
		efficiency[i2] = efficiency[i2] / binCont1
		heavyBack[i2] = heavyBack[i2] / binCont2
		udsBack[i2] = udsBack[i2] / binCont3
		i2 += 1

	eff_array = array.array("f", efficiency)
	heavyBack_array = array.array("f", heavyBack)
	udsBack_array = array.array("f", udsBack)

	c = TCanvas()
	c.SetLogy()
	heavyBack_graph = ROOT.TGraph(bins, eff_array, heavyBack_array)
	heavyBack_graph.SetLineColor(9)
	heavyBack_graph.GetXaxis().SetTitle("Signal rate")
	heavyBack_graph.GetYaxis().SetTitle("Background rate")
	heavyBack_graph.SetMaximum(1)
	heavyBack_graph.SetMinimum(pow(10,-4))
	udsBack_graph = ROOT.TGraph(bins, eff_array, udsBack_array)
	udsBack_graph.SetLineColor(2)
	heavyBack_graph.Draw("A*")
	udsBack_graph.Draw("*")
	img = ROOT.TImage.Create()
	img.FromPad(c)
	img.WriteImage(output)
	del c, img, heavyBack_graph, udsBack_graph, eff_array, heavyBack_array, udsBack_array
	del efficiency, heavyBack, udsBack

def draw_purityPlot(hist1, hist2, hist3, bins, output):
	# Draws purity plot and saves to folder.
	purity = []
	efficiency = []
	binCont1 = binCont2 = binCont3 = 0
	i = bins
	while i > 0:
		binCont1 = binCont1 + hist1.GetBinContent(i)
		binCont2 = binCont2 + hist2.GetBinContent(i)
		binCont3 = binCont3 + hist3.GetBinContent(i)
		purity.append((binCont1)/((binCont1)+((binCont2)+(binCont3))))
		efficiency.append(binCont1)
		i = i - 1
	i=0
	while i < bins:
		efficiency[i] = efficiency[i] / binCont1
		i += 1

	purity_array = array.array("f", purity)
	eff_array = array.array("f", efficiency)
	c = TCanvas()
	purity_graph = ROOT.TGraph(bins, eff_array, purity_array)
	purity_graph.GetXaxis.SetTitle("Efficiency")
	purity_graph.GetYaxis.SetTitle("Purity")


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
	inputCheck, totalEvents = check_input(f)
	if not inputCheck:
		sys.exit(1)

	hists = histsBranchCorrected(f, totalEvents, args.numberOfBins)

	if args.basicHistograms:
		draw_histograms(hists[8],hists[6],hists[10],outputPlots[0])
		draw_histograms(hists[7],hists[9],hists[11],outputPlots[1])

	if args.backgroundPlots:
		draw_backgroundPlots(hists[8],hists[6],hists[10],args.numberOfBins,outputPlots[2])
		draw_backgroundPlots(hists[7],hists[9],hists[11],args.numberOfBins,outputPlots[3])		

	print "done"

if __name__=='__main__':
	main()