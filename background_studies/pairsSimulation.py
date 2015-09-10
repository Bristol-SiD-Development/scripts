#! /bin/env python2
from subprocess import check_call, call
import argparse
import os

def parse_args():
	# Takes in arguments from the command line!!!
	current_directory = os.getcwd()

	parser = argparse.ArgumentParser("Run the SiD reco chain")

	parser.add_argument("pairsInput",help="Path to the pairs.dat input file")
	
	parser.add_argument("-o", "--output_name",
						help="Final output name", required=True)

	parser.add_argument("-n", "--numberOfParticles",
						help="Number of MCParticles to use from pairs file")

	return parser.parse_args()

def run_conversion(converter, pairsInput, number):
	print "#### Running Conversion to stdhep..."
	binLib=converter+"/bin:"+converter+"/lib/*"
	if number:
		check_call(["java", "-cp", binLib,
					"PairsToStdhepLCIO",
					"-i", pairsInput,
					"-o", "converterOutput.stdhep",
					"-n", number])
	elif not number:
		check_call(["java", "-cp", binLib,
					"PairsToStdhepLCIO",
					"-i", pairsInput,
					"-o", "converterOutput.stdhep"])

	print "#### Done"

def run_slic(slic, geometry, number, macro, tbl):
	print "#### Running Slic simulation..."
	if number:
		check_call([slic, "-g", geometry,
					"-i", "converterOutput.stdhep",
					"-o", "slicOutput.slcio",
					"-m", macro, 
					"-r", number,
					"-P", tbl])
	elif not number:
		check_call([slic, "-g", geometry,
					"-i", "converterOutput.stdhep",
					"-o", "slicOutput.slcio",
					"-m", macro, 
					"-r", "500000",
					"-P", tbl])

	print "#### Done"

def merge_events(lcsim, steeringFile):
	print "#### Merging Events with lcsim..."

	check_call(["java", "-jar", lcsim, steeringFile])

	print "#### Done"

def main():
	args = parse_args()

	# List of all the things needed. This needs to be personalised by you.
	converter="/afs/cern.ch/user/j/jtingey/GP/GuineaPig_conversion"
	slic="/cvmfs/ilc.desy.de/sw/x86_64_gcc44_sl6/v01-17-08/slic/ilcsoft-v01-17-07/bin/slic"
	lcsim="/afs/cern.ch/user/j/jtingey/GP/merge_events/lcsim-distribution-3.1.3-bin.jar"
	geometry="/afs/cern.ch/user/j/jtingey/ILC_DBD/detectors/sidloi3/sidloi3.lcdd"
	macro="/afs/cern.ch/user/j/jtingey/GP/defaultILCCrossingAngle.mac"
	tbl="/cvmfs/ilc.desy.de/sw/x86_64_gcc44_sl6/v01-17-08/slic/ilcsoft-v01-17-07/data/particle.tbl"
	merge="merge.xml"

	# Run the conversion of pairs.dat file to stdhep.
	run_conversion(converter, args.pairsInput, args.numberOfParticles)

	# Run SLIC on this stdhep file.
	run_slic(slic, geometry, args.numberOfParticles, macro, tbl)

	# Cleanup of the converter output file
	os.remove("converterOutput.stdhep")

	# Merge the events in the SLIC output file into one event. 
	merge_events(lcsim, merge)

	# Cleanup only leaving the final output file
	os.remove("slicOutput.slcio")
	os.rename("mergeOutput.slcio", args.output_name)
	
	print "#### FINISHED ####"

if __name__=="__main__":
	main()