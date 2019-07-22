import matlab.engine
import numpy as np
import subprocess
import os

# generate inputs
eng = matlab.engine.start_matlab()
target_dir = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\input_meshes\\target'
files = [f for f in os.listdir(target_dir)]
for file in files:
    print(file)
    eng.eval("output_directory = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\results';", nargout = 0)
    eng.workspace['target_filename'] = os.path.join(target_dir, file)
    eng.eval("source_filename = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\17_07_19\\input_meshes\\source\\ObjetSynthetique_simp32.ply';", nargout = 0)
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
    full_output_dir = eng.eval("generate_inputs_for_FPFH_algorithm(output_directory, source_filename, target_filename, theta, rot_axis, trans, scale_coeff, cutting_plane, ratio, nb_pc_target, type_of_noise, noise_generation, nb_noise_matrix_source, noise_level_source, nb_noise_matrix_target, noise_level_target);")
    #[full_output_dir, scale_source, scale_target] = eng.eval("generate_inputs_for_FPFH_algorithm(output_directory, source_filename, target_filename, theta, rot_axis, trans, scale_coeff, cutting_plane, ratio, nb_pc_target, type_of_noise, noise_generation, nb_noise_matrix_source, noise_level_source, nb_noise_matrix_target, noise_level_target);", nargout = 3)
    #print("source scale = ", scale_source)
    #print("target scale = ", scale_target)
    
# process inputs (center and normalize)
#pcd_files_source = []
#pcd_files_target = []
#files = [f for f in os.listdir(full_output_dir)]


#for file in files:
    #if '.pcd' in file and '_source_' in file:
        #pcd_files_source.append(os.path.join(full_output_dir, file))
    #elif '.pcd' in file and '_target_' in file:
        #pcd_files_target.append(os.path.join(full_output_dir, file))



#for source_file in pcd_files_source:
    #for target_file in pcd_files_target:
        #[source_scale, target_scale] = eng.process_input_data(source_file,target_file, nargout=2)