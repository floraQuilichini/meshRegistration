import matlab.engine
import numpy as np
import subprocess
import os


full_output_dir = "C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\results\\theta1.57_t0_10_6X"


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
#sub_source = 4.0
sub_target = 1.0

eng = matlab.engine.start_matlab()

#for f in pcd_files_source:
    #voxel_side_size_source = eng.compute_voxel_size(eng.pcread(f), sub_source)
    #print(voxel_side_size_source)
	
for f in pcd_files_target:	
    voxel_side_size_target = eng.compute_voxel_size(eng.pcread(f), sub_target)
    print(voxel_side_size_target)


    # compute FPFH features
executable_FPFH = "C:/Registration/FPFH/generateFPFH_files/x64/Release/generateFPFH_files.exe"

for f in pcd_files_source:
    pointCloud_random_down = eng.pcdownsample(eng.pcread(f),'random',0.5); # random downsampling 60% of the point cloud
    parts = f.rsplit('.', 1)
    pc_down_filename = parts[0] + "_downsampled." + parts[1]
    eng.pcwrite(pointCloud_random_down,pc_down_filename,'Encoding','ascii', nargout = 0);
    args = executable_FPFH + " " + pc_down_filename + " " + str(0) + " " + str(voxel_side_size_target*2.0) + " " + str(voxel_side_size_target*5.0) # compute FPFH
    subprocess.call(args, stdin=None, stdout=None, stderr=None)

for f in pcd_files_target:
    args = executable_FPFH + " " + f + " " + str(0) + " " + str(voxel_side_size_target*2.0) + " " + str(voxel_side_size_target*5.0)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)