#! /bin/env python2

from subprocess import check_call
import argparse

def parse_args(steering_files, geometry_files):
    #Note that is impossible to set the weight and probability options that marlin takes because the resulting string would have multiple '.'s in it... 
    current_directory = os.getcwd()
    
    default_steering_dir = os.path.join(current_directory, "steering_files")
    default_geometry_dir = os.path.join(current_directory, "geometry_files")

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
                        help="Number of events to run per job",
                        default=10)
    parser.add_argument("-n", "--num-jobs",
                        help="Number of jobs to run",
                        default=1)

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


def main():
    steering_files = setup_steering_dict()
    geometry_files = setup_geom_dict()
    args = get_args(steering_files, geometry_files)

    return 0
if __name__ == "__main__":
    main()
