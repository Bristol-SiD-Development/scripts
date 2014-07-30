#! /bin/env python2

import subprocess
import argparse
import os

def run_geom_conv(geom_conv_jar, file_format, input_filename, output_filename):
    
    subprocess.check_call(['java','-jar', geom_conv_jar,'-o', file_format, input_filename, output_filename])

def generate_output_filename(compactxml_filename, file_format):
    base_name = compactxml_filename.rsplit('_', 1)[0]
    if (file_format == "lcdd"):
        return base_name + "_lcdd.lcdd"
    elif (file_format == "pandora"):
        return base_name + "_pandora.xml"
    

def file_geom_conv(geom_conv_jar, file_format, input_list_filename, output_list_filename, output_folder):
    input_list_file = open(os.path.join(os.getcwd(), input_list_filename),'r')
    output_list_file = open(os.path.join(os.getcwd(), output_list_filename), 'w')
    for input_filename in input_list_file.readlines():
        input_filename = input_filename.strip('\n')
        output_filename = os.path.join(os.getcwd(), output_folder, generate_output_filename(os.path.basename(input_filename), file_format))
        run_geom_conv(geom_conv_jar, file_format, input_filename, output_filename)
        output_list_file.write(output_filename + '\n')
    output_list_file.close()
        
def folder_geom_conv(geom_conv_jar, file_format, input_folder, output_list_filename, output_folder):
    # Search folder for all *compact.xml files
    # Generate text file containing all files to be converted
    input_list_filename = os.path.join(os.getcwd(), output_folder, "compactxml_input_list.txt")
    output_list_filename = os.path.join(os.getcwd(), output_folder, output_list_filename)
    input_list_file = open(input_list_filename, 'w')
    for input_filename in os.listdir(input_folder):
        if input_filename.endswith("_compact.xml"):
            input_list_file.write(os.path.join(os.getcwd(), input_folder, input_filename) + '\n')
    input_list_file.close()
    # Convert using file_geom_conv with specified output folder
    file_geom_conv(geom_conv_jar, file_format, input_list_filename, output_list_filename, os.path.join(os.getcwd(), output_folder))
    

def main(args):
    run_geom_conv(*args)
    return 0

if __name__ == "__main__":
    # insert argument parsing here! For now will just use a list of filenames
    geom_conv_jar = "/afs/cern.ch/eng/clic/software/GeomConverter/GeomConverter-2_4/target/GeomConverter-2.4-bin.jar"
    file_format = "lcdd"
    input_file = "input.xml"
    output_file = "output.lcdd"
    args = [geom_conv_jar,file_format,input_file,output_file]
    main(args)
