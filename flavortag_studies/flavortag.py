from subprocess import check_call, call
import argparse
import os
import os.path
import os.path as path
import sys

def parse_args():
	current_directory = os.getcwd()
	parser = argparse.ArgumentParser("Run flavortagging through Marlin...")

	parser.add_argument("dst_input",help="Path to DST file outputed from main chain...")

	parser.add_argument("-s", "--steering_file",
						help="Path to the JetClustering and Flavortag steeringfile.xml",
						default="/afs/cern.ch/user/j/jtingey/ILC_DBD/steeringFiles/marlinFlavortag.xml")

	parser.add_argument("-g", "--gear_file",
						help="Path to the gear file for the detector used",
						default="/afs/cern.ch/user/j/jtingey/ILC_DBD/steeringFiles/sidloi3.gear")

	parser.add_argument("-o", "--output_directory",
						help="name of output file",
						default=current_directory)

	parser.add_argument("-m", "--marlin",
						help="Marlin executable to run on",
						default="/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05/Marlin/v01-05/bin/Marlin")
	return parser.parse_args()

def check_paths(input_file,steering_file,gear_file,output_directory,marlin):
	all_files_good = True
	if not os.path.isfile(input_file):
		print "Error: Input file does not exist."
		all_files_good = False
	if not os.path.exists(output_directory):
		print "Error: Output directory does not exist."
		all_files_good = False
	if not os.path.isfile(steering_file):
		print "Error: Steering file does not exist."
		all_files_good = False
	if not os.path.isfile(gear_file):
		print "Error: Gear file does not exist."
		all_files_good = False	
	if not os.path.isfile(marlin):
		print "Error: Marlin does not exist."
		all_files_good = False	
	return all_files_good

def output_file(input_file,output_directory):
	input_dir, input_file_ext = os.path.splitext(input_file)
	input_name = path.basename(input_dir)
	output_name = input_name.replace("_DST","_flavortag.slcio")
	output = os.path.join(output_directory,output_name) 
	print "Output = " +output
	return output

def main():
	args = parse_args()

	print "\n####################"
	print "## Running Marlin ##"
	print "##  Flavortagging ##"
	print "####################"

	print "\nInputFile = " + args.dst_input
	print "SteeringFile =" + args.steering_file
	print "GearFile = " + args.gear_file
	print "Marlin = " + args.marlin

	paths = check_paths(args.dst_input,args.steering_file,args.gear_file,args.output_directory,args.marlin)
	if not paths:
		sys.exit(1)

	output = output_file(args.dst_input,args.output_directory)

	print "\nRunning Marlin Flavortagging..."

	check_call( [args.marlin, 
		   "--global.LCIOInputFiles=" + args.dst_input,
		   "--global.GearXMLFile=" + args.gear_file,
		   "--MyLCIOOutputProcessor.LCIOOutputFile=" + output,
		   args.steering_file])

	if not os.path.isfile(output):
		print "\nMarlin does not seem to have created its output file. Aborting..."
		sys.exit(1)

	print "\nDone..."

	return 0

if __name__=='__main__':
	main()