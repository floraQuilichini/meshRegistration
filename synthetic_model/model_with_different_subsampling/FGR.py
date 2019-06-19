import numpy as np
import subprocess
import os

# call Fast Registration algorithm	
executable_FGR = "C:\\FastGlobalRegistration-build\\FastGlobalRegistration\\Release\\FastGlobalRegistration.exe"
full_output_dir = "C:\\Registration_meshes\\synthetic_model\\test\\target_with_lower_number_of_points\\KL_distance\\theta1.57_t0_10_20Z\\with_cut_with_target_and_source_noise_with_rotation\\temp2"
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
        source_att = source_name[0].split('_source_')
        source_prop = source_att[-1]
        output_file = output_prefix + source_prop + target_prop + output_ext
        args = executable_FGR + " " + os.path.join(full_output_dir, source_file) + " " + os.path.join(full_output_dir, target_file) + " " + output_file + " " + initial_matching + " " + cross_check
        subprocess.call(args, stdin=None, stdout=None, stderr=None)