import os, sys, argparse, os.path
import ROOT
import array

from ROOT import *

def basic_histogram(filename):
	tags = filename.Get("tags")
	hist = ROOT.TH1F("tag","tag",100,0,1)
	tags.Project("tag", "tag")


def main():
	input_files = ["/home/jooosh25/summerInstall/ZPoleBBar100kFlavortag/rootOutputBBar.root",
				   "/home/jooosh25/summerInstall/ZPoleccbar10KFlavortag/rootOutputCCbar.root",
				   "/home/jooosh25/summerInstall/ZPoleuds10KFlavortag/rootOutputuds.root"]

	f1 = ROOT.TFile(input_files[0], "READ")
	f2 = ROOT.TFile(input_files[1], "READ")
	f3 = ROOT.TFile(input_files[2], "READ")

	tags1 = f1.Get("tags")
	tags2 = f2.Get("tags")
	tags3 = f3.Get("tags")

	bhist1 = ROOT.TH1F("btag1","btag1",100,0,1)
	bhist2 = ROOT.TH1F("btag2","btag2",100,0,1)
	bhist3 = ROOT.TH1F("btag3","btag3",100,0,1)
	chist1 = ROOT.TH1F("ctag1","ctag1",100,0,1)
	chist2 = ROOT.TH1F("ctag2","ctag2",100,0,1)
	chist3 = ROOT.TH1F("ctag3","ctag3",100,0,1)	

	tags1.Project("btag1", "btag")
	tags2.Project("btag2", "btag")
	tags3.Project("btag3", "btag")
	tags1.Project("ctag1", "ctag")
	tags2.Project("ctag2", "ctag")
	tags3.Project("ctag3", "ctag")

	c = TCanvas()
	c.SetLogy()

	bhist1.SetLineColor(kBlue)
	bhist2.SetLineColor(kGreen)
	bhist3.SetLineColor(kRed)

	bhist1.Draw("same")
	bhist2.Draw("same")
	bhist3.Draw("same")

	input1 = raw_input()

	del c

	c = TCanvas()
	c.SetLogy()

	chist1.SetLineColor(kBlue)
	chist2.SetLineColor(kGreen)
	chist3.SetLineColor(kRed)

	chist1.Draw("same")
	chist2.Draw("same")
	chist3.Draw("same")

	input1 = raw_input()

	del c

	i = 100

	bcont1 = 0
	bcont2 = 0
	bcont3 = 0
	ccont1 = 0
	ccont2 = 0
	ccont3 = 0
	beff = []
	bcback = []
	budsback = []
	bpur = []
	ceff = []
	cbback = []
	cudsback = []
	cpur = []

	while i > 0:
		bcont1 = bcont1 + bhist1.GetBinContent(i)
		bcont2 = bcont2 + bhist2.GetBinContent(i)
		bcont3 = bcont3 + bhist3.GetBinContent(i)
		ccont1 = ccont1 + chist1.GetBinContent(i)
		ccont2 = ccont2 + chist2.GetBinContent(i)
		ccont3 = ccont3 + chist3.GetBinContent(i)
		beff.append(bcont1 / 20000)
		bcback.append(bcont2 / 20000)
		budsback.append(bcont3 / 20000)
		ceff.append(ccont2 / 20000)
		cbback.append(ccont1 / 20000)
		cudsback.append(ccont3 / 20000)
		#bpurity = (bcont1*0.1512)/((bcont1*0.1512)+((bcont2*0.1203)+(bcont3*0.2720)))
		#cpurity = (ccont2*0.1203)/((ccont2*0.1203)+((ccont1*0.1512)+(ccont3*0.2720)))
		bpurity = (bcont1)/((bcont1)+((bcont2)+(bcont3)))
		cpurity = (ccont2)/((ccont2)+((ccont1)+(ccont3)))
		bpur.append(bpurity)
		cpur.append(cpurity)
		i = i - 1

	beff_array = array.array("f", beff)
	bcback_array = array.array("f", bcback)
	budsback_array = array.array("f", budsback)
	bpur_array = array.array("f", bpur)
	ceff_array = array.array("f", ceff)
	cbback_array = array.array("f", cbback)
	cudsback_array = array.array("f", cudsback)
	cpur_array = array.array("f", cpur)

	c = TCanvas()
	c.SetLogy()

	bbackc = ROOT.TGraph(100, beff_array, bcback_array)
	bbackc.SetLineColor(kGreen)
	bbackc.GetXaxis().SetTitle("Signal rate")
	bbackc.GetYaxis().SetTitle("Background rate")
	bbackc.SetMaximum(1)
	bbackc.SetMinimum(pow(10,-4))
	bbackuds = ROOT.TGraph(100, beff_array, budsback_array)
	bbackuds.SetLineColor(kRed)
	bbackc.Draw("A*")
	bbackuds.Draw("*")

	input1 = raw_input()

	del c

	c = TCanvas()
	c.SetLogy()

	cbackb = ROOT.TGraph(100, ceff_array, cbback_array)
	cbackb.SetLineColor(kBlue)
	cbackb.GetXaxis().SetTitle("Signal rate")
	cbackb.GetYaxis().SetTitle("Background rate")
	cbackb.SetMaximum(1)
	cbackb.SetMinimum(pow(10,-4))
	cbackuds = ROOT.TGraph(100, ceff_array, cudsback_array)
	cbackuds.SetLineColor(kRed)
	cbackb.Draw("A*")
	cbackuds.Draw("*")

	input1 = raw_input()

	del c

	c = TCanvas()

	burity = ROOT.TGraph(100, beff_array, bpur_array)
	burity.GetXaxis().SetTitle("Efficiency")
	burity.GetYaxis().SetTitle("Purity")
	burity.SetMaximum(1.1)
	burity.SetMinimum(0.2)
	curity = ROOT.TGraph(100, ceff_array, cpur_array)
	burity.Draw("A*")
	curity.Draw("*")

	input1 = raw_input()

	del c

if __name__=='__main__':
	main()