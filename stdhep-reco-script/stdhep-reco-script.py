#! /bin/env python2

from subprocess import check_call, call
import argparse

import os

def parse_args(steering_files, geometry_files):
    #Note that is impossible to set the weight and probability options that marlin takes because the resulting string would have multiple '.'s in it... 
    current_directory = os.getcwd()
    
    default_steering_dir = os.path.join(current_directory, "steering_files")
    default_geometry_dir = os.path.join(current_directory, "geometry_files")
    #default_weight_dir = os.path.join(current_directory, "weight_files")
    #default_weight_prefix = "qq91_v02_p01"
    #default_prob_dir = os.path.join(current_directory, "prob_files")

    parser = argparse.ArgumentParser("Run the SiD reco chain")

    parser.add_argument("stdhep_input",help="Path to the stdhep input file" )
    
    parser.add_argument("-s", "--steering-dir", 
                        help="Path to the directory containing the following files: " + ", ".join([steering_files[key] for key in steering_files]),
                        default=default_steering_dir)
    
    parser.add_argument("-g", "--geometry-dir", 
                        help="Path to the directory containing the following files: "  + ", ".join([geometry_files[key] for key in geometry_files]),
                        default=default_geometry_dir)
    
    parser.add_argument("-o", "--output-dir",
                        help="Path to the output directory",
                        default=current_directory)
    parser.add_argument("-r", "--runs",
                        help="Number of events to run",
                        default=10)
    parser.add_argument("-S", "--skip-num",
                        help="Number of events to skip at the start of the file",
                        default=0)
    parser.add_argument("-d" ,"--delete-intermediate-files",
                        help="Deletes intermediate (all except the last) files as they become useless to save on disk usage. Defaults to False (as the intermediate files may be useful)",
                        action='store_true')
    return parser.parse_args()

def setup_steering_dict():
    steering_files = {"lcsim_digi":"lcsim_prepandora.xml", 
                      "lcsim_track_strat":"lcsim_tracking_strategies.xml", 
                      "pandora":"pandora.xml", 
                      "marlin_vertexing":"marlin_vertexing.xml",
                      "lcsim_dst":"lcsim_postpandora.xml", 
                      "marlin_flavortag":"marlin_flavortag.xml"}
    return steering_files

def setup_geom_dict():
    geometry_files = {"slic":"geom_slic.lcdd",
                      "pandora":"geom_pandora.xml",
                      "marlin":"geom_marlin_gear.xml"}


    return geometry_files
def setup_binary_dict(ilcsoft_dir):
    #slic_binary="/afs/cern.ch/eng/clic/software/slic/2.9.8/rhel5_i686_gcc/packages/slic/v2r9p8/bin/Linux-g++/slic" 
    #slic_binary=os.path.join(ilcsoft_dir,"slic/v03-01-03/build/bin/slic")
    slic_binary="/afs/cern.ch/eng/clic/software/slic/2.9.8/rhel5_i686_gcc/scripts/slic.sh"
    pandora_binary=os.path.join(ilcsoft_dir, "slicPandora/v01-00-00/build/bin/PandoraFrontend")
    marlin_binary=os.path.join(ilcsoft_dir,"Marlin/v01-05/bin/Marlin")
    anajob_binary=os.path.join(ilcsoft_dir,"lcio/v02-04-03/bin/anajob")

    lcsim_jar="/afs/cern.ch/eng/clic/software/lcsim/lcsim-2_5/target/lcsim-2.5-bin.jar"

    binaries = {"slic": slic_binary,
                "lcsim": lcsim_jar,
                "pandora": pandora_binary,
                "marlin": marlin_binary,
                "anajob": anajob_binary}
    return binaries


def setup_output_dicts(input_file, extension, output_dir):
    input_dir, input_file_ext = os.path.split(input_file)

    input_file_no_ext, stdhep_ext = os.path.splitext(input_file_ext)
    slcio_ext = ".slcio"

    slic_output_file_no_ext = input_file_no_ext + "_slic" #needed because slic wants the output path and filenames split into two arguments!
    slic_output_file = slic_output_file_no_ext + slcio_ext

    slic_output              = os.path.join(output_dir,slic_output_file)

    lcsim_digi_output        = os.path.join(output_dir, input_file_no_ext + "_lcsimDigi" + slcio_ext)
    pandora_output           = os.path.join(output_dir, input_file_no_ext + "_pandora" + slcio_ext)
    marlin_vertexing_output  = os.path.join(output_dir, input_file_no_ext + "_marlinVertexing" + slcio_ext)
    lcsim_dst_output         = os.path.join(output_dir, input_file_no_ext + "_lcsimDst" + slcio_ext)
    lcsim_full_output        = os.path.join(output_dir, input_file_no_ext + "_lcsimFull" + slcio_ext)
    marlin_flavortag_output  = os.path.join(output_dir, input_file_no_ext + "_lcfiPlusFlavourTag" + slcio_ext)

    output_paths_dict = {"slic": slic_output,
                         "lcsim_digi":lcsim_digi_output,
                         "pandora":pandora_output,
                         "marlin_vert":marlin_vertexing_output,
                         "lcsim_dst":lcsim_dst_output,
                         "lcsim_full":lcsim_full_output,
                         "marlin_flav":marlin_flavortag_output}

    #Only used for slic but may as well do all of them
    output_names_dict = {}
    for key in output_paths_dict:
        output_dir, output_name = os.path.split(output_paths_dict[key])
        output_names_dict[key] = output_name

    return output_names_dict, output_paths_dict

def check_all_paths_in_dict_exist(file_dict):
    all_files_good = True
    for key in file_dict:
        if not os.path.isfile(file_dict[key]):
            print "[^] Error! no valid \"" + str(key) + "\" found. \"" + str(file_dict[key]) + "\" is not valid!!"
            all_files_good = False
    if not all_files_good:
        return False
    return True
    
def main():
    ilcsoft_dir="/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05"

    steering_files = setup_steering_dict()
    geometry_files = setup_geom_dict()
    binaries = setup_binary_dict(ilcsoft_dir)

    args = parse_args(steering_files, geometry_files)

    if not args:
        print "Invalid args"
        return -1

    #Add the path to the steering and geometry dirs to the file names
    for key in steering_files:
        steering_files[key] = os.path.join(args.steering_dir, steering_files[key])

    for key in geometry_files:
        geometry_files[key] = os.path.join(args.geometry_dir, geometry_files[key])

    #Error checking is good
    if not check_all_paths_in_dict_exist(steering_files):
        return -1
    if not check_all_paths_in_dict_exist(geometry_files):
        return -1

    if not os.path.isdir(args.output_dir):
        print "[^] Error no valid output dir found. \"" + str(args.output_dir) + "\" is not valid!!" 

    output_names_dict, output_paths_dict = setup_output_dicts(args.stdhep_input, ".slcio", args.output_dir) #we need names for slic as it doesn't seem to able to take in a single full path

    print "[^]Running CLIC's version of slic (through their bash script)..."
    check_call([binaries["slic"], 
                "-g", geometry_files["slic"],
                "-i", args.stdhep_input,
                "-o", output_names_dict["slic"],
                " --skip-events", args.skip_num,
                "-p", args.output_dir[:-1], #remove the trailing '/' so it doesn't break because slic does filepaths like a concussed puppy (this is probably not a portable solution...)
                "-r", args.runs
                ])

    if not os.path.isfile(output_paths_dict["slic"]):
        print "[^] Error! Slic doesn't seem to have created its output file. Aborting..."
        return -1

    #Probably worth pointing this out...
    print "[^] Warning! slic has returned 0 but it does this even if it screws up!!"

    print "[^] Running ilcsoft's lcsim"
    check_call(["java", "-jar", binaries["lcsim"],
                steering_files["lcsim_digi"],
                "-DinputFile=" +  output_paths_dict["slic"],
                "-DoutputFile=" + output_paths_dict["lcsim_digi"],
                "-DtrackingStrategies=" + steering_files["lcsim_track_strat"]
                ])
    
    if not os.path.isfile(output_paths_dict["lcsim_digi"]):
        print "[^] Error! lcsim digitisation doesn't seem to have created its output file. Aborting..."
        return -1

    if args.delete_intermediate_files:
        print "[^] Warning! Deleting slic's output file..."
        os.remove(output_paths_dict["slic"])

    print "[^] Adding pandora libraries to path..."
    old_LD_LIBRARY_PATH = os.path.expandvars("$LD_LIBRARY_PATH") #We need to restore this before marlin can run
    os.putenv("$LD_LIBRARY_PATH", "{0}:{1}".format(os.path.join(ilcsoft_dir, "slicPandora/v01-00-00/build/lib"),old_LD_LIBRARY_PATH))

    print "[^] Running pandora..."
    check_call([binaries["pandora"], 
           "-g",  geometry_files["pandora"],
           "-c",  steering_files["pandora"],
           "-i",  output_paths_dict["lcsim_digi"],
           "-o",  output_paths_dict["pandora"]])


    if not os.path.isfile(output_paths_dict["pandora"]):
        print "[^] Error! pandora doesn't seem to have created its output file. Aborting..."
        return -1

    if args.delete_intermediate_files:
        print "[^] Warning! Deleting lcsim digitisation output file..."
        os.remove(output_paths_dict["lcsim_digi"])

    print "[^] Removing pandora libraries from path..."
    os.putenv("$LD_LIBRARY_PATH", old_LD_LIBRARY_PATH)

    print "[^] Running marlin vertexing..."
    check_call([binaries["marlin"],
           "--global.LCIOInputFiles=" + output_paths_dict["pandora"],
           "--MyLCIOOutputProcessor.LCIOOutputFile="+  output_paths_dict["marlin_vert"],
           steering_files["marlin_vertexing"]
           ])

    if not os.path.isfile(output_paths_dict["marlin_vert"]):
        print "[^] Error! marlin vertexing doesn't seem to have created its output file. Aborting..."
        return -1

    if args.delete_intermediate_files:
        print "[^] Warning! Deleting pandora output file..."
        os.remove(output_paths_dict["pandora"])


    print "[^] Running lcsim dsting..."
    check_call(["java", "-jar", binaries["lcsim"],
           steering_files["lcsim_dst"],
           "-DinputFile=" + output_paths_dict["marlin_vert"],
           "-DrecFile=" + output_paths_dict["lcsim_full"],
           "-DdstFile=" + output_paths_dict["lcsim_dst"]])

    if not os.path.isfile(output_paths_dict["lcsim_dst"]):
        print "[^] Error! lcsim dsting doesn't seem to have created its output file. Aborting..."
        return -1

    if args.delete_intermediate_files:
        print "[^] Warning! Deleting marlin vertexing output file..."
        os.remove(output_paths_dict["marlin_vert"])

    print "[^] Running marlin flavortagging..."
    check_call( [binaries["marlin"], 
           "--global.LCIOInputFiles=" + output_paths_dict["lcsim_dst"],
           "--global.GearXMLFile=" + geometry_files["marlin"],
           "--MyLCIOOutputProcessor.LCIOOutputFile=" + output_paths_dict["marlin_flav"],
           steering_files["marlin_flavortag"]])

    if not os.path.isfile(output_paths_dict["marlin_flav"]):
        print "[^] Error! marlin flavortagging doesn't seem to have created its output file. Aborting..."
        return -1

    if args.delete_intermediate_files:
        print "[^] Warning! Deleting lcsim dsting output file..."
        os.remove(output_paths_dict["lcsim_dst"])

    return 0
    
if __name__=="__main__":
    main()
