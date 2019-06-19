import matlab.engine
import numpy as np
import subprocess
import os

# generate inputs
eng = matlab.engine.start_matlab()
target_dir = 'C:\\Registration_meshes\\synthetic_model\\model_with_different_subsampling\\target_mesh_lowerSampling'
files = [f for f in os.listdir(target_dir)]
for file in files:
    print(file)
    eng.eval("output_directory = 'C:\\Registration_meshes\\synthetic_model\\test\\target_with_lower_number_of_points\\KL_distance';", nargout = 0)
    eng.workspace['target_filename'] = os.path.join(target_dir, file)
    eng.eval("source_filename = 'C:\\Registration_meshes\\synthetic_model\\model_with_different_subsampling\\model_mesh\\ObjetSynthetique_simp32.ply';", nargout = 0)
    eng.eval("nb_pc_target = 1;", nargout = 0);
    eng.eval("type_of_noise = 'gaussian';", nargout = 0)
    eng.eval("noise_generation = 'auto';", nargout = 0)
    eng.eval("noise_level_source  = 0.3", nargout = 0)
    eng.eval("noise_level_target = 0.5;", nargout = 0)
    eng.eval("nb_noise_matrix_source = 1;", nargout = 0)
    eng.eval("nb_noise_matrix_target = 1;", nargout = 0)
    eng.eval("cutting_plane = 'XZ';", nargout = 0)
    eng.eval("ratio = 0.4;", nargout = 0)
    eng.eval("theta = 3.14/2;", nargout = 0)
    eng.eval("rot_axis = 'Z';", nargout = 0)
    eng.eval("trans = [0, 10, 20];", nargout = 0)
    eng.eval("scale_coeff = [0.5, 0.5, 0.5];", nargout = 0)
    [full_output_dir, scale_source, scale_target] = eng.eval("generate_inputs_for_FPFH_algorithm(output_directory, source_filename, target_filename, theta, rot_axis, trans, scale_coeff, cutting_plane, ratio, nb_pc_target, type_of_noise, noise_generation, nb_noise_matrix_source, noise_level_source, nb_noise_matrix_target, noise_level_target);", nargout = 3)
    print("source scale = ", scale_source)
    print("target scale = ", scale_target)