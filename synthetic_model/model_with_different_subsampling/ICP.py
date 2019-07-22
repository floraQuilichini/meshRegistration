# compute ICP registration
import numpy as np
import subprocess
import os
from shutil import copyfile



input_files_dir = "C:\\Registration\\Test\\meshRegistration\\synthetic_model\\18_07_19\\results\\theta1.57_t0_10_6X\\m0_s0_m0_s0\\edgeCollapse"
output_subdir = "ICP"
pcd_target_file = "ObjetSynthetique_simp64_edgeCollapse_target_m0_s0_XZ0.4.pcd"
pcd_source_file = "ObjetSynthetique_simp32_source_m0_s0.pcd"


#create ICP directory
os.mkdir(os.path.join(input_files_dir, output_subdir))
copyfile(os.path.join(input_files_dir, pcd_target_file), os.path.join(input_files_dir, output_subdir, pcd_target_file))
copyfile(os.path.join(input_files_dir, pcd_source_file), os.path.join(input_files_dir, output_subdir, pcd_source_file))


# compute ICP registration
cloudCompare_exe = "C:\\Program Files\\CloudCompare\\CloudCompare.exe"
registered_pc_name = "registered_pc.pcd"
args = cloudCompare_exe + " -o " + os.path.join(input_files_dir, output_subdir, pcd_target_file) + " -o " + os.path.join(input_files_dir, output_subdir, pcd_source_file) + " -NO_TIMESTAMP -AUTO_SAVE OFF -ICP -RANDOM_SAMPLING_LIMIT 3500 -C_EXPORT_FMT PCD -SAVE_CLOUDS FILE " + os.path.join(input_files_dir, output_subdir, registered_pc_name) + " FILE " + os.path.join(input_files_dir, output_subdir, pcd_source_file) # data file first and reference file second 
subprocess.call(args, stdin=None, stdout=None, stderr=None)


# compute point cloud to point cloud distance 
log_file = os.path.join(input_files_dir, output_subdir, 'log.txt')
open(log_file, 'a').close()
result_file = os.path.join(input_files_dir, output_subdir, 'icp_cc_results.txt')
open(result_file, 'a').close()
args = cloudCompare_exe + " -o " + os.path.join(input_files_dir, output_subdir, registered_pc_name) + " -o " + os.path.join(input_files_dir, output_subdir, pcd_source_file) + " -NO_TIMESTAMP -C_EXPORT_FMT ASC -c2c_dist -LOG_FILE " + log_file  # compared file first and reference file second
subprocess.call(args, stdin=None, stdout=None, stderr=None)


f=open(log_file, "r")
fl = f.readlines()
for line in fl:
    if "[ComputeDistances]" in line: 
        out_file =open(result_file, "a+")
        out_file.write("%s" % line)
        out_file.close()
f.close()