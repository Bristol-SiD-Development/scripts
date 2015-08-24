#! /bin/env python2

from subprocess import check_call
import argparse
from datetime import datetime 
import os
import stat #so we can make the scripts executable
def parse_args(steering_files, geometry_files):
    #Note that is impossible to set the weight and probability options that marlin takes because the resulting string would have multiple '.'s in it... 
    current_directory = os.getcwd()
    
    default_steering_dir = os.path.join("/afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/", "steering_files")
    default_geometry_dir = os.path.join("/afs/cern.ch/user/o/oreardon/public/ilc/scripts/stdhep-reco-script/", "sidloi3_edited")

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
    parser.add_argument("-q", "--batch-queue",
                        help="Queue to submit to (see the bsub command)",
                        default="8nh")
    parser.add_argument("-n", "--num-jobs",
                        help="Number of jobs to run",
                        default=1,
                        type=int)
    parser.add_argument("-S", "--skip-num",
                        help="Number of events to skip (useful so you don't overlap with previous runs)",
                        default=1,
                        type=int)

    """parser.add_argument("-d" ,"--delete-intermediate-files",
                        help="Deletes intermediate (all except the last) files as they become useless to save on disk usage. Defaults to False (as the intermediate files may be useful)",
                        action='store_true')
    
                        """
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

    args = parse_args(steering_files, geometry_files)

    current_directory = os.getcwd()

    #We'll make a timestamped directory to put all our (tempory) job submission scripts in
    script_time_str = datetime.now().isoformat()
    script_dir = os.path.join(current_directory, "job_scripts_{0}".format(script_time_str)) 
    os.makedirs(script_dir)

    job_indices = range(0, args.num_jobs)

    #just set up a couple of lists of empty strings for now. We'll put the useful stuff in them in a bit
    script_paths = [""]*args.num_jobs 
    job_output_dirs = [""]*args.num_jobs
    job_final_output_paths = [""]*args.num_jobs

    #Put the useful stuff in them
    for job_index in job_indices:
        script_paths[job_index] = os.path.join(script_dir, "{0}.sh".format(job_index))
        
        job_output_dirs[job_index] = os.path.join(args.output_dir, "job_{0}".format(job_index))

        input_dir, input_file_ext = os.path.split(args.stdhep_input)
        input_file_no_ext, stdhep_ext = os.path.splitext(input_file_ext)
        slcio_ext = ".slcio"
        
        job_final_output_paths[job_index] = os.path.join(job_output_dirs[job_index], input_file_no_ext + "_lcfiPlusFlavourTag" + slcio_ext)

        os.makedirs(job_output_dirs[job_index])
        
        #I'm so sorry for this....
        #We construct a varaiant of the submit-stdhep-reco-script.sh script
        script_string ='#! /bin/bash \n\
# Timestamp {0} \n\
# Script number {1} \n\
ilcsoft_version=v01-17-05 \n\
ilcsoft_root=/afs/desy.de/project/ilcsoft/sw/x86_64_gcc44_sl6 \n\
ilcsoft_root_dir=$ilcsoft_root/$ilcsoft_version \n\
echo "Sourcing init_ilcsoft.sh..." \n\
source $ilcsoft_root_dir/init_ilcsoft.sh \n\
/afs/cern.ch/user/o/oreardon/public/ilc/scripts_again/scripts/stdhep-reco-script/stdhep-reco-script.py \\\n\
-o {2}/ \\\n\
-r {3} \\\n\
-d \\\n\
--skip-num {4} \\\n\
-s {5} \\\n\
-g {6} \\\n\
--final-output-file {7} \\\n\
{8}'.format(script_time_str, job_index, job_output_dirs[job_index], args.runs, args.skip_num + job_index*int(args.runs), args.steering_dir, args.geometry_dir, job_final_output_paths[job_index],  args.stdhep_input)

        #write it to disk
        script_file = open(script_paths[job_index], "wb")
        print >> script_file, script_string
        script_file.close()

        #make it executable, readable and writiable by everyone
        os.chmod(script_paths[job_index],  stat.S_IRUSR ^ stat.S_IWUSR ^ stat.S_IXUSR  ^ stat.S_IROTH ^ stat.S_IWOTH ^ stat.S_IXOTH ^ stat.S_IRGRP ^ stat.S_IWGRP ^ stat.S_IXGRP)

        #stick the script in the queue
        check_call(["bsub",
                    "-q", args.batch_queue, 
                    script_paths[job_index],
                    "-J", str(job_index)]) 
        
    lcfiPlus_files_file = open(os.path.join(args.output_dir, "job_output_files_{0}.txt".format(script_time_str)),"w")
    for job_final_output_path in job_final_output_paths:
        print >> lcfiPlus_files_file, job_final_output_path
    lcfiPlus_files_file.close()
    return 0


if __name__ == "__main__":
    main()

