from subprocess import check_call, call
import argparse, os, sys, os.path
# from trackProb import TrackProb
# import ROOT
# from ROOT import *

def parse_args(): 
	current_directory = os.getcwd()

	parser = argparse.ArgumentParser("Produce weights files for LCFIPlus flavortagging...")
	
	parser.add_argument("-b", "--bbbarSample", help="path to bbbarSample.slcio or sample folder, DST input",
						default="input/pythiaZPolebbbar_sidloi3_0_v3r0p3_HEAD_ILC_DBD_0116_DST.slcio")

	parser.add_argument("-c", "--ccbarSample", help="path to ccbarSample.slcio or sample folder, DST input",
						default="input/pythiaZPoleccbar_sidloi3_0_v3r0p3_HEAD_ILC_DBD_0116_DST.slcio")

	parser.add_argument("-q", "--qqbarSample", help="path to qqbarSample.slcio or sample folder, DST input",
						default="input/pythiaZPoleuds_sidloi3_0_v3r0p3_HEAD_ILC_DBD_0116_DST.slcio")

	parser.add_argument("-g", "--gearFile", help="Input gear file",
						default="input/sidloi3.gear")

	return parser.parse_args()

def input_files(bbbar, ccbar, qqbar):
	# Checks input and returns lists of input files.
	bbbarInput = []
	ccbarInput = []
	qqbarInput = []
	if os.path.isdir(bbbar) and os.path.isdir(ccbar) and os.path.isdir(qqbar):
		for filename in os.listdir(bbbar):
			name, extension = os.path.splitext(filename)
			if extension not in [".slcio"]:
				print "ERROR: The file " + filename + " is not valid!"
			else:
				bbbarInput.append(os.path.join(bbbar, filename))
				print os.path.join(bbbar,filename) + " VALID!"
		for filename in os.listdir(ccbar):
			name, extension = os.path.splitext(filename)
			if extension not in [".slcio"]:
				print "ERROR: The file " + filename + " is not valid!"
			else:
				ccbarInput.append(os.path.join(ccbar, filename))
				print os.path.join(ccbar,filename) + " VALID!"
		for filename in os.listdir(qqbar):
			name, extension = os.path.splitext(filename)
			if extension not in [".slcio"]:
				print "ERROR: The file " + filename + " is not valid!"
			else:
				qqbarInput.append(os.path.join(qqbar, filename))
				print os.path.join(qqbar,filename) + " VALID!"

	elif os.path.exists(bbbar) and os.path.exists(ccbar) and os.path.exists(qqbar):
		bbbarInput.append(bbbar)
		print bbbar + " VALID!"
		ccbarInput.append(ccbar)
		print ccbar + " VALID!"
		qqbarInput.append(qqbar)
		print qqbar + " VALID!"

	else: 
		print "ERROR: Input not valid, need 3 directories or 3 files with .slcio extension... Exiting!"
		sys.exit(1)

	return bbbarInput, ccbarInput, qqbarInput

def makentuple(input_file, marlin, gearFile):
	# Runs a file through makentuple in LCFIPlus...
	print "Running " + input_file + " through makentuple"
	name, ext = os.path.splitext(input_file)
	outputName = os.path.basename(name) + "_make"
	check_call([marlin, 
		   "--global.LCIOInputFiles=" + input_file,
		   "--global.GearXMLFile=" + gearFile,
		   "steeringFiles/makentuple2.xml"])
	os.rename("ntuple.root", outputName + ".root")
	return outputName + ".root"

def trackntuple(input_file, marlin, gearFile):
	print "Running " + input_file + " through trackntuple"
	# Run a file through trackntuple in LCFIPlus...
	name, ext = os.path.splitext(input_file)
	outputName = os.path.basename(name) + "_track"
	check_call([marlin, 
		   "--global.LCIOInputFiles=" + input_file,
		   "--global.GearXMLFile=" + gearFile,
		   "steeringFiles/trackntuple.xml"])
	os.rename("tracks.root", outputName + ".root")
	return outputName + ".root"

def train(marlin, gearFile):
	check_call([marlin, 
			"--global.GearXMLFile=" + gearFile,
			"steeringFiles/train2.xml"])

def combine(hadd, output, rootlist):
	haddlist = []
	for item in rootlist:
		haddlist.append(item)

	haddlist.append(output)
	haddlist.append(hadd)
	haddlist.reverse()
	check_call(haddlist)

def clean(bOutput, cOutput, qOutput, file1, file2, file3):
	for rootFile in bOutput:
		os.remove(rootFile)
	for rootFile in cOutput:
		os.remove(rootFile)
	for rootFile in qOutput:
		os.remove(rootFile)
	os.remove(file1)
	os.remove(file2)
	os.remove(file3)

def TrackProb(root):
	call([root, '-q', '-b', 
		 'TrackProb.C(\"btracks.root\",\"ctracks.root\",\"qtracks.root\",\"d0test.root\",\"z0test.root\")'])

def main():
	# Need to ensure 'init_ilcsoft.sh' has been sourced for these to work! (v01-17-08 seems to work)
	marlin = "Marlin"
	hadd = "hadd"
	root = "root"
	args = parse_args()

	if not args:
		print "ERROR: Arguments not valid... Exiting!"
		sys.exit(1)

	# Checks input and puts all input files from a directory into a list!!! 
	if args.bbbarSample and args.ccbarSample and args.qqbarSample:
		binput, cinput, qinput = input_files(args.bbbarSample, args.ccbarSample, args.qqbarSample)

	else:
		print "ERROR: Invalid input... Exiting!"
		sys.exit(1)

	bOutput = []
	cOutput = []
	qOutput = []

	# Runs the files through trackntuple, to make prop.root files
	for input_file in binput:
		bOutput.append(trackntuple(input_file, marlin, args.gearFile))
	for input_file in cinput:
		cOutput.append(trackntuple(input_file, marlin, args.gearFile))
	for input_file in qinput:
		qOutput.append(trackntuple(input_file, marlin, args.gearFile))

	print "#### Combining tracks.root files"

	# Combine root files using hadd!
	combine(hadd, "btracks.root", bOutput)
	combine(hadd, "ctracks.root", cOutput)
	combine(hadd, "qtracks.root", qOutput)

	# Run the TrackProb.C macro in root on these file to make the vtxprob files.
	TrackProb(root) # Change so you can specify input names	

	# Cleans all intermediate files from this first stage!
	clean(bOutput, cOutput, qOutput, "btracks.root", "ctracks.root", "qtracks.root")

	# Reset the output lists back to empty
	bOutput = []
	cOutput = []
	qOutput = []

	# Run the input files through makentuple, to make train.root files
	for input_file in binput:
		bOutput.append(makentuple(input_file, marlin, args.gearFile))
	for input_file in cinput:
		cOutput.append(makentuple(input_file, marlin, args.gearFile))
	for input_file in qinput:
		qOutput.append(makentuple(input_file, marlin, args.gearFile))

	print "#### Combining make.root files"

	# Again combine files.
	combine(hadd, "bb.root", bOutput)
	combine(hadd, "cc.root", cOutput)
	combine(hadd, "qq.root", qOutput)

	# Run trainMVA on the three root files to make the weights, this currently crashes when make the c2 weights.
	train(marlin, args.gearFile)

	# Clean the intermediate files from this stage!
	clean(bOutput, cOutput, qOutput, "bb.root", "cc.root", "qq.root")

	print "[DONE]"

if __name__=="__main__":
	main()