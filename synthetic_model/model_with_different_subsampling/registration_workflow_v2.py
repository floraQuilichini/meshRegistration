# whole registration workflow

import matlab.engine
import numpy as np
import subprocess
import os
import sys
from shutil import copyfile


#input parameters
full_output_dir = sys.argv[1]
source_name = sys.argv[2]
target_name = sys.argv[3]
fraction_kept_points = float(sys.argv[4])


eng = matlab.engine.start_matlab()

# downsample source point cloud 
    # get source pcd file
pcd_source_file = source_name + ".pcd"
    # downsampling
#fraction_kept_points = 0.5; 
pointCloud_random_down = eng.pcdownsample(eng.pcread(os.path.join(full_output_dir, pcd_source_file)),'random',fraction_kept_points); # random downsampling 50% of the point cloud
    # save downsampled point cloud
pc_down_filename = source_name + "_downsampled" + str(fraction_kept_points) + ".pcd"
eng.pcwrite(pointCloud_random_down,os.path.join(full_output_dir, pc_down_filename),'Encoding','ascii', nargout = 0)


# compute FPFH
executable_FPFH = "C:/Registration/FPFH/generateFPFH_files/x64/Release/generateFPFH_files.exe"
    # get target pcd file
pcd_target_file = target_name + ".pcd"
voxel_side_size_source = eng.compute_voxel_size(eng.pcread(os.path.join(full_output_dir, pc_down_filename)), 1.0)
    # compute voxel size
voxel_side_size_target = eng.compute_voxel_size(eng.pcread(os.path.join(full_output_dir, pcd_target_file)), 1.0)
voxel_size = eng.max(voxel_side_size_target, voxel_side_size_source)
    # compute FPFH for source
args = executable_FPFH + " " + os.path.join(full_output_dir, pc_down_filename) + " " + str(0) + " " + str(voxel_size*2.0) + " " + str(voxel_size*5.0)
subprocess.call(args, stdin=None, stdout=None, stderr=None)
    # compute FPFH for target
args = executable_FPFH + " " + os.path.join(full_output_dir, pcd_target_file) + " " + str(0) + " " + str(voxel_size*2.0) + " " + str(voxel_size*5.0)
subprocess.call(args, stdin=None, stdout=None, stderr=None)
    
    
# FGR
executable_FGR = "C:\\Registration\\FGR\\FastGlobalRegistration-build\\FastGlobalRegistration\\Release\\FastGlobalRegistration.exe"
output_prefix = "output_"
output_ext = ".txt"
initial_matching = 'True'
cross_check = 'True'
    # get source and target binary file
source_bin_file = source_name + "_downsampled" + str(fraction_kept_points) + ".bin"
target_bin_file = target_name + ".bin"    
    # compute registration
output_file = output_prefix + source_name +"_downsampled" + str(fraction_kept_points) + "_" + target_name + output_ext
args = executable_FGR + " " + os.path.join(full_output_dir, source_bin_file) + " " + os.path.join(full_output_dir, target_bin_file) + " " + os.path.join(full_output_dir, output_file) + " " + initial_matching + " " + cross_check
subprocess.call(args, stdin=None, stdout=None, stderr=None)


# process registration
eng.eval("scale_coeff = [1, 1, 1];", nargout = 0)
registered_target_file = eng.pcSimpleRegistration(full_output_dir, output_file, full_output_dir, eng.eval('scale_coeff'))

# compute target registered to source distance
cloudCompare_exe = "C:\\Program Files\\CloudCompare\\CloudCompare.exe"
log_file = os.path.join(full_output_dir, 'log.txt')
open(log_file, 'a').close()
fgr_cc_result_file = os.path.join(full_output_dir, 'cc_results.txt')
open(fgr_cc_result_file, 'a').close()
print(registered_target_file)
args = cloudCompare_exe + " -o " + registered_target_file + " -o " + os.path.join(full_output_dir, pcd_source_file) + " -C_EXPORT_FMT ASC -c2c_dist -LOG_FILE " + log_file  # compared file first and reference file second
subprocess.call(args, stdin=None, stdout=None, stderr=None)

# process cloudCompare output
header = "objet source : " + source_name + " , downsampling : " + str(fraction_kept_points) + " ; objet target : " + target_name + "\n"
out_file =open(fgr_cc_result_file, "a+")
out_file.write("%s" % header)
out_file.close()

f=open(log_file, "r")
fl = f.readlines()
for line in fl:
    if "[ComputeDistances]" in line: 
        out_file =open(fgr_cc_result_file, "a+")
        out_file.write("%s" % line)
        out_file.close()
f.close()
