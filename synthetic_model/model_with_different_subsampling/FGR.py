import numpy as np
import subprocess
import os

# call Fast Registration algorithm	
executable_FGR = "C:\\Registration\\FGR\\FastGlobalRegistration-build\\FastGlobalRegistration\\Release\\FastGlobalRegistration.exe"
full_output_dir = "C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\results\\theta1.57_t0_10_6X"
output_prefix = full_output_dir + "\\output_"
output_ext = ".txt"
initial_matching = 'True';
cross_check = 'True';

	# get all the bin files in the subdirectory
source_bin_files = []
target_bin_files = []

files = [f for f in os.listdir(full_output_dir)]

for file in files:
    print(file)
    if '.bin' in file and 'source' in file:
        source_bin_files.append(file)
    elif '.bin' in file and 'target' in file:
        target_bin_files.append(file)


for target_file in target_bin_files:
    target_name = target_file.rsplit('.', 1)
    target_att = target_name[0].split('_target_')
    target_prop = target_att[-1]
    for source_file in source_bin_files:
        source_name = source_file.rsplit('.', 1)
        print(source_name)
        source_att = (source_name[0].split('_source_'))[-1].rsplit('_', 1)
        print(source_att)
        source_prop = source_att[0]
        print(source_prop)
        output_file = output_prefix + source_prop + "_" + target_prop + output_ext
        args = executable_FGR + " " + os.path.join(full_output_dir, source_file) + " " + os.path.join(full_output_dir, target_file) + " " + output_file + " " + initial_matching + " " + cross_check
        subprocess.call(args, stdin=None, stdout=None, stderr=None)