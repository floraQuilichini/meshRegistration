import matlab.engine
import numpy as np
import subprocess
import os

# generate inputs
eng = matlab.engine.start_matlab()
eng.eval("output_directory = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\test';", nargout = 0)
eng.eval("source_filename = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\model_with_different_subsampling\\ObjetSynthetique_simp32.ply';", nargout = 0)
eng.eval("target_filename = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\model_with_different_subsampling\\ObjetSynthetique_simp32_remeshed.ply';", nargout = 0)
eng.eval("nb_pc_target = 1;", nargout = 0);
eng.eval("type_of_noise = 'gaussian';", nargout = 0)
eng.eval("noise_generation = 'auto';", nargout = 0)
eng.eval("noise_level_source  = 0;", nargout = 0)
eng.eval("noise_level_target = 0;", nargout = 0)
eng.eval("nb_noise_matrix_source = 0;", nargout = 0)
eng.eval("nb_noise_matrix_target = 0;", nargout = 0)
eng.eval("cutting_plane = 'XZ';", nargout = 0)
eng.eval("ratio = 0;", nargout = 0)
eng.eval("theta = 0;", nargout = 0)
eng.eval("rot_axis = 'Z';", nargout = 0)
eng.eval("trans = [0, 0, 0];", nargout = 0)
eng.eval("scale_coeff = [0.5, 0.5, 0.5];", nargout = 0)

full_output_dir = eng.eval("generate_inputs_for_FPFH_algorithm(output_directory, source_filename, target_filename, theta, rot_axis, trans, scale_coeff, cutting_plane, ratio, nb_pc_target, type_of_noise, noise_generation, nb_noise_matrix_source, noise_level_source, nb_noise_matrix_target, noise_level_target);")


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
scale_coeff = eng.eval("scale_coeff")

for f in pcd_files_source:
    voxel_side_size_source = eng.compute_voxel_size(eng.pcread(f), sub_source)
    print(voxel_side_size_source)
	
for f in pcd_files_target:	
    voxel_side_size_target = eng.compute_voxel_size(eng.pcread(f), sub_target)
    print(voxel_side_size_target)	


	# compute FPFH features
executable_FPFH = "C:/Registration/FPFH/generateFPFH_files/x64/Release/generateFPFH_files.exe"
for f in pcd_files_source:
    args = executable_FPFH + " " + f + " " + str(0) + " " + str(2*voxel_side_size_source) + " " + str(5*voxel_side_size_source)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)

for f in pcd_files_target:
    args = executable_FPFH + " " + f + " " + str(0) + " " + str(2*voxel_side_size_target) + " " + str(5*voxel_side_size_target)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)	
	