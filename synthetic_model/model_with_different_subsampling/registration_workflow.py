# whole registration workflow

import matlab.engine
import numpy as np
import subprocess
import os



#input parameters
source_filename = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\input_meshes\\source\\ObjetSynthetique_simp32.ply'
target_dir = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\input_meshes\\target'
#target_filename = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\input_meshes\\target\\ObjetSynthetique_simp64_edge_collapse.ply'
output_directory = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\results'

eng = matlab.engine.start_matlab()
files = [f for f in os.listdir(target_dir)]
for file in files:
    eng.workspace['output_directory'] = output_directory
    eng.workspace['source_filename'] = source_filename
    #eng.workspace['target_filename'] = target_filename
    eng.workspace['target_filename'] = os.path.join(target_dir, file)
    eng.eval("nb_pc_target = 1;", nargout = 0)
    eng.eval("type_of_noise = 'gaussian';", nargout = 0)
    eng.eval("noise_generation = 'auto';", nargout = 0)
    eng.eval("noise_level_source  = 0.3", nargout = 0)
    eng.eval("noise_level_target = 0.5;", nargout = 0)
    eng.eval("nb_noise_matrix_source = 1;", nargout = 0)
    eng.eval("nb_noise_matrix_target = 1;", nargout = 0)
    eng.eval("cutting_plane = 'XZ';", nargout = 0)
    eng.eval("ratio = 0.4;", nargout = 0)
    eng.eval("theta = 3.14/2;", nargout = 0)
    eng.eval("rot_axis = 'X';", nargout = 0)
    eng.eval("trans = [0, 10, 6];", nargout = 0)
    eng.eval("scale_coeff = [1, 1, 1];", nargout = 0)
    # generate input data (source and target files)
    full_output_dir = eng.eval("generate_inputs_for_FPFH_algorithm(output_directory, source_filename, target_filename, theta, rot_axis, trans, scale_coeff, cutting_plane, ratio, nb_pc_target, type_of_noise, noise_generation, nb_noise_matrix_source, noise_level_source, nb_noise_matrix_target, noise_level_target);")

# downsample source point cloud 
    # get source and target pcd files
pcd_files_source = []
pcd_files_target = []
files = [f for f in os.listdir(full_output_dir)]


for file in files:
    if '.pcd' in file and '_source_' in file:
        pcd_files_source.append(os.path.join(full_output_dir, file))
    elif '.pcd' in file and '_target_' in file:
        pcd_files_target.append(os.path.join(full_output_dir, file))

    # downsampling
source_pcd_file = pcd_files_source[0]
fraction_kept_points = 0.5; 
pointCloud_random_down = eng.pcdownsample(eng.pcread(source_pcd_file),'random',fraction_kept_points); # random downsampling 50% of the point cloud
    # save downsampled point cloud
parts = source_pcd_file.rsplit('.', 1)
pc_down_filename = parts[0] + "_downsampled" + str(fraction_kept_points) + "." + parts[1]
eng.pcwrite(pointCloud_random_down,pc_down_filename,'Encoding','ascii', nargout = 0)


# compute FPFH
executable_FPFH = "C:/Registration/FPFH/generateFPFH_files/x64/Release/generateFPFH_files.exe"
voxel_side_size_source = eng.compute_voxel_size(eng.pcread(pc_down_filename), 1.0)
for f_target in pcd_files_target:
    # compute voxel size
    voxel_side_size_target = eng.compute_voxel_size(eng.pcread(f_target), 1.0)
    voxel_size = eng.max(voxel_side_size_target, voxel_side_size_source)
    # compute FPFH for source
    args = executable_FPFH + " " + pc_down_filename + " " + str(0) + " " + str(voxel_size*2.0) + " " + str(voxel_size*5.0)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)
    # compute FPFH for target
    args = executable_FPFH + " " + f_target + " " + str(0) + " " + str(voxel_size*2.0) + " " + str(voxel_size*5.0)
    subprocess.call(args, stdin=None, stdout=None, stderr=None)
    
    
# FGR
executable_FGR = "C:\\Registration\\FGR\\FastGlobalRegistration-build\\FastGlobalRegistration\\Release\\FastGlobalRegistration.exe"
output_prefix = full_output_dir + "\\output_"
output_ext = ".txt"
initial_matching = 'True'
cross_check = 'True'

	# get source and target binary file
source_bin_files = []
target_bin_files = []
files = [f for f in os.listdir(full_output_dir)]

for file in files:
    if '.bin' in file and 'source' in file:
        source_bin_files.append(file)
    elif '.bin' in file and 'target' in file:
        target_bin_files.append(file)

    # compute registration
source_bin_file = source_bin_files[0]
for target_file in target_bin_files:
    target_name_ext = target_file.rsplit('.', 1)
    target_name = target_name_ext[0]
    #target_att = target_name.split('_target_')
    #target_prop = target_att[-1]
    source_name_ext = source_bin_file.rsplit('.', 1)
    source_name = source_name_ext[0]
    #source_att = (source_name.split('_source_'))[-1].rsplit('_', 1)
    #source_prop = source_att[0]
    #output_file = output_prefix + source_prop + "_" + target_prop + output_ext
    output_file = output_prefix + source_name + "_" + target_name + output_ext
    args = executable_FGR + " " + os.path.join(full_output_dir, source_bin_file) + " " + os.path.join(full_output_dir, target_file) + " " + output_file + " " + initial_matching + " " + cross_check
    subprocess.call(args, stdin=None, stdout=None, stderr=None)


# process registration
registered_target_files = eng.pcRegistration(full_output_dir, full_output_dir, full_output_dir, eng.eval('scale_coeff'))
if type(registered_target_files) is str:
    registered_target_files = registered_target_files.split()
    

# compute target registered to source distance
cloudCompare_exe = "C:\\Program Files\\CloudCompare\\CloudCompare.exe"
log_file = os.path.join(full_output_dir, 'log.txt')
open(log_file, 'a').close()
result_file = os.path.join(full_output_dir, 'cc_results.txt')
open(result_file, 'a').close()

for target_registered_file in registered_target_files:
    print(target_registered_file)
    args = cloudCompare_exe + " -o " + target_registered_file + " -o " + source_pcd_file + " -C_EXPORT_FMT ASC -c2c_dist -split_xyz -LOG_FILE " + log_file  # compared file first and reference file second
    subprocess.call(args, stdin=None, stdout=None, stderr=None)
    # process cloudCompare output
    f=open(log_file, "r")
    fl = f.readlines()
    for line in fl:
        if "[ComputeDistances]" in line: 
            output_file =open(result_file, "a+")
            output_file.write("%s" % line)
            output_file.close()
    f.close()
