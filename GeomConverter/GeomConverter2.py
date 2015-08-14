#! /bin/env python2

import subprocess
import argparse
import os

def parse_args():
	current_dir = os.getcwd()
	geom_jar_default="/afs/cern.ch/eng/clic/software/GeomConverter/GeomConverter-2_4/target/GeomConverter-2.4-bin.jar"
	parser = argparse.ArgumentParser("Run the Geometry Converter...")

	parser.add_argument("compact_input",help="Path to compact.xml input file")

	parser.add_argument("-l", "--lcdd_format",
						help="Produces lcdd format output",
						action='store_true')

	parser.add_argument("-p", "--pandora_format",
						help="Produces Pandora.xml format output",
						action='store_true')

	parser.add_argument("-r", "--heprep_format",
						help="Produces heprep formmat output",
						action='store_true')

	parser.add_argument("-o", "--output_dir",
						help="Path to output directory",
						default=current_dir)

	parser.add_argument("-j", "--geom_converter_jar",
						help="Path to GeomConverter jar",
						default=geom_jar_default)

	return parser.parse_args()

def setup_format_dictionary(lcdd_format, pandora_format, heprep_format):
	required_formats={}
	if lcdd_format:
		required_formats["lcdd"]="lcdd"
	if pandora_format:
		required_formats["pandora"]="pandora"
	if heprep_format:
		required_formats["heprep"]="heprep"
	return required_formats

def setup_output_files(input_file, output_dir, lcdd_format, pandora_format, heprep_format):
	output_files={}
	base_name, extension = os.path.splitext(input_file)
	if lcdd_format:
		output_files["lcdd"] = os.path.join(output_dir, base_name + "_lcdd.lcdd")
	if pandora_format:
		output_files["pandora"] = os.path.join(output_dir, base_name + "_pandora.xml")
	if heprep_format:
		output_files["heprep"] = os.path.join(output_dir, base_name + "_heprep.heprep")
	return output_files

def main():
	
	args = parse_args()

	if not args:
		print "Invalid args"
		return -1

	format_dict=setup_format_dictionary(args.lcdd_format,args.pandora_format,args.heprep_format)

	output_files=setup_output_files(args.compact_input, args.output_dir, args.lcdd_format,args.pandora_format,args.heprep_format)

	print "Running Geometry Converter..."

	for key in format_dict:
		print "Converting to " + format_dict[key] + "..."
		subprocess.check_call(['java','-jar', args.geom_converter_jar,'-o', format_dict[key], args.compact_input, output_files[key]])
		print "    OUTPUT -> " + output_files[key]

	print "----Complete----"

	return 0

if __name__=="__main__":
	main()
