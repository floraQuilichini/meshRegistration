import matlab.engine
import subprocess
import os

# generate inputs
eng = matlab.engine.start_matlab()
eng.eval("output_directory = 'C:\\Users\\fquilich\\Documents\\MATLAB';", nargout = 0)
eng.eval("pc_filename = 'C:\\Registration_meshes\\synthetic_model\\mesh_bruite\\simp32\\halfedge_collapse\\ObjetSynthetique_simp32.ply';", nargout = 0)
eng.eval("nb_pc_target = 1;", nargout = 0);
eng.eval("type_of_noise = 'gaussian';", nargout = 0)
eng.eval("noise_generation = 'auto';", nargout = 0)
eng.eval("noise_level_source  = 0.3;", nargout = 0)
eng.eval("noise_level_target = 1.0;", nargout = 0)
eng.eval("nb_noise_matrix_source = 1;", nargout = 0)
eng.eval("nb_noise_matrix_target = 2;", nargout = 0)
eng.eval("cutting_plane = 'XZ';", nargout = 0)
eng.eval("ratio = 0.4;", nargout = 0)
eng.eval("theta = 3.14/2;", nargout = 0)
eng.eval("rot_axis = 'X';", nargout = 0)
eng.eval("trans = [0, 10, 6];", nargout = 0)

full_output_dir = eng.eval("generate_inputs_for_FPFH_algorithm(output_directory, pc_filename, theta, rot_axis, trans, cutting_plane, ratio, nb_pc_target, type_of_noise, noise_generation, nb_noise_matrix_source, noise_level_source, nb_noise_matrix_target, noise_level_target);")


# compute FPFH descriptors
	# get the voxel size
eng.eval("sub = 4;", nargout = 0)
voxel_side_size = eng.eval("compute_voxel_size(pcread(pc_filename), sub); ")

	# get all the pcd files in the subdirectory

pcd_files = []
files = [f for f in os.listdir(full_output_dir)]
print(files)


for file in files:
	if '.pcd' in file:
		pcd_files.append(os.path.join(full_output_dir, file))


	# compute FPFH features
executable_FPFH = "C:/FPFH/generateFPFH_files/x64/Release/generateFPFH_files.exe"
for f in pcd_files:
    args = executable_FPFH + " " + f + " " + str(voxel_side_size)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)
	

# call Fast Registration algorithm	
executable_FGR = "C:\\FastGlobalRegistration-build\\FastGlobalRegistration\\Release\\FastGlobalRegistration.exe"
output_prefix = full_output_dir + "\\output_"
output_ext = ".txt"

	# get all the bin files in the subdirectory
source_bin_files = []
target_bin_files = []



for file in files:
	if '.bin' in file and 'source' in file:
		source_bin_files.append(file)
	elif '.bin' in file and 'target' in file:
		target_bin_files.append(file)


for target_file in target_bin_files:
    target_name = target_file.rsplit('.', 1)
    print(target_name)
    target_att = target_name[0].split('_target_')
    print(target_att)
    target_prop = target_att[-1]
    print(target_prop)
    for source_file in source_bin_files:
        source_name = source_file.rsplit('.', 1)
        source_att = source_name[0].split('_source_')
        source_prop = source_att[-1]
        output_file = output_prefix + source_prop + target_prop + output_ext
        args = executable_FGR + " " + source_file + " " + target_file + " " + output_file
        subprocess.call(args, stdin=None, stdout=None, stderr=None)
		

# check registration

for file in files:
	if '.txt' in file and 'output_' in file:
		eng.pcRegistration(full_output_dir, full_output_dir, nargout=0)
			

