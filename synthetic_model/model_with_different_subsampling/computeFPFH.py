import matlab.engine
import numpy as np
import subprocess
import os


full_output_dir = "C:\\Registration_meshes\\synthetic_model\\test\\target_with_lower_number_of_points\\KL_distance\\theta1.57_t0_10_20Z\\with_cut_with_target_and_source_noise_with_rotation"


# compute FPFH descriptors

	# get all the pcd files in the subdirectory
pcd_files_source = []
pcd_files_target = []
files = [f for f in os.listdir(full_output_dir)]


for file in files:
    if '.pcd' in file and '_source_' in file:
        pcd_files_source.append(os.path.join(full_output_dir, file))
    elif '.pcd' in file and '_target_' in file:
        pcd_files_target.append(os.path.join(full_output_dir, file))


	# get the voxel size
sub_source = 1.0
sub_target = 1.0

eng = matlab.engine.start_matlab()

for f in pcd_files_source:
    voxel_side_size_source = eng.compute_voxel_size(eng.pcread(f), sub_source)
    print(voxel_side_size_source)
	
for f in pcd_files_target:	
    voxel_side_size_target = eng.compute_voxel_size(eng.pcread(f), sub_target)
    print(voxel_side_size_target)	


	# compute FPFH features
executable_FPFH = "C:/FPFH/generateFPFH_files/x64/Release/generateFPFH_files.exe"
for f in pcd_files_source:
    args = executable_FPFH + " " + f + " " + str(0) + " " + str(2*voxel_side_size_source) + " " + str(5*voxel_side_size_source)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)

for f in pcd_files_target:
    args = executable_FPFH + " " + f + " " + str(0) + " " + str(2*voxel_side_size_target) + " " + str(5*voxel_side_size_target)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)	
	