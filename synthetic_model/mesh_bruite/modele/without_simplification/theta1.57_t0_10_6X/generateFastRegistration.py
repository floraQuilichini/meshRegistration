import subprocess
import os

executable = "C:\\FastGlobalRegistration-build\\FastGlobalRegistration\\Release\\FastGlobalRegistration.exe"
input_source = "C:\\Users\\fquilich\\Documents\\MATLAB\\theta1.57_t0_10_6X\\ObjetSynthetique_simp32_up_m0_s0XZ.bin"
input_target = "C:\\Users\\fquilich\\Documents\\MATLAB\\theta1.57_t0_10_6X\\modele.bin"
output_file = "C:\\Users\\fquilich\\Documents\\MATLAB\\theta1.57_t0_10_6X\\output.txt"


args = executable + " " + input_source + " " + input_target + " " + output_file
subprocess.call(args, stdin=None, stdout=None, stderr=None)

