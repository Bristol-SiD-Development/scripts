from subprocess import check_call, call
import argparse, os, sys, os.path

def parse_args(): 
	current_directory = os.getcwd()

	parser = argparse.ArgumentParser("Produce weights files for LCFIPlus flavortagging...")
	
	parser.add_argument("-b", "--bbbarSample", help="path to bbbarSample.slcio or sample folder, DST input",
						default="input/pythiaZPole_sidloi3_2_DST.slcio")

	parser.add_argument("-c", "--ccbarSample", help="path to ccbarSample.slcio or sample folder, DST input",
						default="input/pythiaZPoleccbar_sidloi3_0_DST.slcio")

	parser.add_argument("-q", "--qqbarSample", help="path to qqbarSample.slcio or sample folder, DST input",
						default="input/pythiaZPoleuds_sidloi3_0_DST.slcio")

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
	# Runs a file through makentuple in LCFIPlus
	name, ext = os.path.splitext(input_file)
	outputName = os.path.basename(name)
	check_call([marlin, 
		   "--global.LCIOInputFiles=" + input_file,
		   "--global.GearXMLFile=" + gearFile,
		   "steeringFiles/makentuple2.xml"])
	os.rename("ntuple.root", outputName + ".root")
	return outputName + ".root"

def combine(hadd, output, rootlist):
	rootlist.append(output)
	rootlist.append(hadd)
	rootlist.reverse()
	check_call(rootlist)

def train(marlin, gearFile):
	check_call([marlin, 
			"--global.GearXMLFile=" + gearFile,
			"steeringFiles/train2.xml"])

def clean(bOutput, cOutput, uOutput):
	for rootFile in bOutput:
		os.remove(rootFile)
	for rootFile in cOutput:
		os.remove(rootFile)
	for rootFile in uOutput:
		os.remove(rootFile)
	os.remove("bb.root")
	os.remove("cc.root")
	os.remove("uu.root")

def main():
	# marlin = "/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05/Marlin/v01-05/bin/Marlin"
	# hadd = "/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05/root/5.34.10/bin/hadd"

	# marlin = "/cvmfs/ilc.desy.de/sw/x86_64_gcc44_sl6/v01-17-08/Marlin/v01-07/bin/Marlin"
	# hadd = "/cvmfs/ilc.desy.de/sw/x86_64_gcc44_sl6/v01-17-08/root/5.34.30/bin/hadd"

	marlin = "Marlin"
	hadd = "hadd"

	args = parse_args()

	if not args:
		print "ERROR: Arguments not valid... Exiting!"
		sys.exit(1)

	if args.bbbarSample and args.ccbarSample and args.qqbarSample:
		binput, cinput, uinput = input_files(args.bbbarSample, args.ccbarSample, args.qqbarSample)

	else:
		print "ERROR: Invalid input... Exiting!"
		sys.exit(1)

	gearFile = args.gearFile

	bOutput = []
	cOutput = []
	uOutput = []

	for input_file in binput:
		bOutput.append(makentuple(input_file, marlin, gearFile))

	for input_file in cinput:
		cOutput.append(makentuple(input_file, marlin, gearFile))

	for input_file in uinput:
		uOutput.append(makentuple(input_file, marlin, gearFile))

	if len(bOutput) > 1:
		combine(hadd, "bb.root", bOutput)
	if len(bOutput) == 1:
		os.rename(bOutput[0], "bb.root")

	if len(cOutput) > 1:
		combine(hadd, "cc.root", cOutput)
	if len(cOutput) == 1:
		os.rename(cOutput[0], "cc.root")

	if len(uOutput) > 1:
		combine(hadd, "qq.root", uOutput)
	if len(uOutput) == 1:
		os.rename(uOutput[0], "qq.root")

	train(marlin, gearFile)

	clean(bOutput, cOutput, uOutput)

	print "[DONE]"

if __name__=="__main__":
	main()