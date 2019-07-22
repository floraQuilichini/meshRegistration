import numpy as np
import subprocess
import os

cloudCompare_exe = "C:\\Program Files\\CloudCompare\\CloudCompare.exe"
pc_model_file = "C:\\Registration\\Test\meshRegistration\\synthetic_model\\10_06_19\\check_previous_results\\theta1.57_t0_10_6X\\exp8\ObjetSynthetique_simp32_source_m0_s0.3_.pcd"  #source file
pc_registered_file = "C:\\Registration\\Test\\meshRegistration\\synthetic_model\\10_06_19\\check_previous_results\\theta1.57_t0_10_6X\\exp8\ObjetSynthetique_simp64_target_m0_s0.5XZ.pcd"   #registered target file
log_file = "C:\\Registration\\Test\\meshRegistration\\synthetic_model\\10_06_19\\check_previous_results\\theta1.57_t0_10_6X\\exp8\\log.txt"
result_file = "C:\\Registration\\Test\\meshRegistration\\synthetic_model\\10_06_19\\check_previous_results\\theta1.57_t0_10_6X\\exp8\\cc_results.txt"

# call cloudCompare to compute pointCloud-pointCloud distance
f=open(log_file, "r")
args = cloudCompare_exe + " -o " + pc_registered_file + " -o " + pc_model_file + " -C_EXPORT_FMT ASC -c2c_dist -LOG_FILE " + log_file  # compared file first and reference file second
subprocess.call(args, stdin=None, stdout=None, stderr=None)

# process cloudCompare output
f=open(log_file, "r")
fl = f.readlines()
for line in fl:
    if "[ComputeDistances]" in line: 
        print(line)
        output_file =open(result_file, "a+")
        output_file.write("%s" % line)
        output_file.close()
