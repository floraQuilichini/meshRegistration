import subprocess
import os

current_path = os.path.dirname(os.path.realpath(__file__))
executable = "C:\\FastGlobalRegistration-build\\FastGlobalRegistration\\Release\\FastGlobalRegistration.exe"
output_name_prefix = current_path + "\\output"
output_ext = ".txt"
input_name_target_prefix = "C:\\Registration_meshes\\synthetic_model\\mesh_bruite\\modele\\ObjetSynthetique_clean_full_res_"
input_ext = ".bin"

# get all the pcd files in the subdirectory

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(current_path):
    for file in f:
        if '.bin' in file:
            files.append(os.path.join(r, file))


for target_prop in ["m0_s0.16667", "m0_s0.33333", "m0_s0.5"]:
	input_target_file = input_name_target_prefix + target_prop + input_ext

	for input_source in files:
		dir = input_source.split('\\')
		file = dir[-1]
		filename_ext = file.split('.', 2)
		filename = filename_ext[0]
		filename_att = filename.split('_', 2)
		source_prop = filename_att[2]
		output_file = output_name_prefix + source_prop + target_prop + output_ext
		args = executable + " " + input_source + " " + input_target_file + " " + output_file
		subprocess.call(args, stdin=None, stdout=None, stderr=None)
	