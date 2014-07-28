#! /bin/env python2

from subprocess import check_call
import argparse

import os

import itertools

def parse_args(steering_files, geometry_files):

    current_directory = os.getcwd()
    
    default_steering_dir = os.path.join(current_directory, "steering_files")
    default_geometry_dir = os.path.join(current_directory, "geometry_files")
    default_weight_dir = os.path.join(current_directory, "weight_files")
    default_weight_prefix = "qq91_v02_p01"
    default_prob_dir = os.path.join(current_directory, "prob_files")

    parser = argparse.ArgumentParser("Run the SiD reco chain")

    parser.add_argument("stdhep_input",help="Path to the stdhep input file" )
    
    parser.add_argument("-s", "--steering-dir", 
                        help="Path to the directory containing the following files: " + ", ".join([steering_files[key] for key in steering_files]),
                        default=default_steering_dir)
    
    parser.add_argument("-g", "--geometry-dir", 
                        help="Path to the directory containing the following files: "  + ", ".join([geometry_files[key] for key in geometry_files]),
                        default=default_geometry_dir)

    parser.add_argument("-w", "--weight-dir", 
                        help="Path to the weight files directory",
                        default="default_weight_dir")

    parser.add_argument("-W", "--weight-prefix", 
                        help="Weight file prefix to use",
                        default=default_weight_prefix)

    parser.add_argument("-p", "--prob-dir", 
                        help="Path to the probability files directory",
                        default=default_prob_dir)
    parser.add_argument("-o", "--output-dir",
                        help="Path to the output directory",
                        default=current_directory)
    parser.add_argument("-r", "--runs",
                        help="Number of events to run",
                        default=10)
    return parser.parse_args()

def main(steering_files, geometry_files, binaries, ilcsoft_dir, args):
    current_directory = os.getcwd()
    input_file_no_ext, ext = os.path.splitext(args.stdhep_input)

    slic_output              = os.path.join(args.output_dir, input_file_no_ext + "_slic" + ext)
    lcsim_digi_output        = os.path.join(args.output_dir, input_file_no_ext + "_lcsimDigi" + ext)
    pandora_output           = os.path.join(args.output_dir, input_file_no_ext  + "_pandora" + ext)
    marlin_vertexing_output  = os.path.join(args.output_dir, input_file_no_ext + "_marlinVertexing" + ext)
    lcsim_dst_output         = os.path.join(args.output_dir, input_file_no_ext + "lcsimDst" + ext)
    lcsim_full_output        = os.path.join(args.output_dir, input_file_no_ext + "lcsimFull" + ext)
    marlin_flavortag_output = os.path.join(args.output_dir, input_file_no_ext + "_lcfiPlusFlavourTag" + ext)


    check_call([binaries["slic"], 
           "-g", geometry_files["slic"],
           "-i", args.stdhep_input,
           "-o", slic_output,
           "-p", args.output_dir,
           "-r", args.runs,
           "-P", "/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05/slic/v03-01-03/simulation/particle.tbl"
           ])

    check_call(["java", "-jar", binaries["lcsim"],
           steering_files["lcsim_digi"],
           "-DinputFile=" +  slic_output,
           "-DoutputFile=" + lcsim_digi_output,
           "-DtrackingStrategies=" + steeringFiles["lcsim_track_strat"]
           ])

    old_LD_LIBRARY_PATH = os.environ.get("LD_LIBRARY_PATH")
    os.putenv("LD_LIBRARY_PATH", 
              "{0}:{1}".format(old_LD_LIBRARY_PATH, 
                               os.path.join(ilcsoft_dir, "slicPandora/v01-00-00/build/lib/")))

    check_call([binaries["pandora"], 
           "-g", geometry_files["pandora"],
           "-c", steering_files["pandora"],
           "-i", lcsim_digi_output,
           "-o", pandora_output])

    os.putenv("LD_LIBRARY_PATH", old_LD_LIBRARY_PATH)

    check_call([binaries["marlin"],
           "--global.LCIOInputFiles=" + pandora_output,
           "--MyLCIOOutputProcessor.LCIOOutputFile="+  marlin_vertexing_output,
           steering_files["marlin_vertexing"]
           ])

    check_call(["java", "-jar", binaries["lcsim"],
           steering_files["lcsim_dst"],
           "-DinputFile=" + marlin_vertexing_output,
           "-DrecFile=" + lcsim_full_output,
           "-DdstFile=" + lcsim_dst_output])

    check_call( binaries["marlin"], 
           "--global.LCIOInputFiles=" + lcsim_dst_output,
           "--MyLCIOOutputProcessor.LCIOOutputFile=" + marlin_flavortag_output,
           "--FlavorTag.WeightsDirectory=" + args.weight_dir,
           "--FlavorTag.WeightsPrefix=" + args.weight_prefix,
           "--FlavorTag.D0ProbFileName=" + os.path.join(args.prob_dir, "d0prob_zpole.root"),
           "--FlavorTag.Z0ProbFileName=" + os.path.join(args.prob_dir, "z0prob_zpole.root"),
           steering_files["marlin_flavortag"])

    return 0

if __name__=="__main__":
    steering_files = {"lcsim_digi":"lcsim_prepandora.xml", 
                      "lcsim_track_strat":"lcsim_tracking_strategies.xml", 
                      "pandora":"pandora.xml", 
                      "marlin_vertexing":"marlin_vertexing.xml",
                      "lcsim_dst":"lscim_postpandora.xml", 
                      "marlin_flavortag":"marlin_flavortag.xml"}

    geometry_files = {"slic":"geom_slic.lcdd",
                      "pandora":"geom_pandora.xml",
                      "marlin":"geom_marlin_gear.xml"}

    ilcsoft_dir="/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6/v01-17-05"
    slic_binary=os.path.join(ilcsoft_dir,"slic/v03-01-03/build/bin/slic")
    
    pandora_binary=os.path.join(ilcsoft_dir, "slicPandora/v01-00-00/build/bin/PandoraFrontend")
    marlin_binary=os.path.join(ilcsoft_dir,"Marlin/v01-05/bin/Marlin")
    anajob_binary=os.path.join(ilcsoft_dir,"lcio/v02-04-03/bin/anajob")

    lcsim_jar="/afs/cern.ch/eng/clic/software/lcsim/lcsim-2_5/target/lcsim-2.5-bin.jar"

    binaries = {"slic": slic_binary,
                "lcsim": lcsim_jar,
                "pandora": pandora_binary,
                "marlin": marlin_binary,
                "anajob": anajob_binary}

    check_call([os.path.join(ilcsoft_dir, "init_ilcsoft.sh")])

    args = parse_args(steering_files, geometry_files)
    print args
    for key in steering_files:
        steering_files[key] = os.path.join(args.steering_dir, steering_files[key])

    for key in geometry_files:
        geometry_files[key] = os.path.join(args.geometry_dir, geometry_files[key])

    if args:
        main(steering_files, geometry_files, binaries, ilcsoft_dir, args)
    else:
        print "Invalid args"
