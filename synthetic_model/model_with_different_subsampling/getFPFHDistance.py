import matlab.engine
import numpy as np
import subprocess
import os

full_output_dir = "C:\\Registration\\Test\\meshRegistration\\synthetic_model\\10_06_19\\no_scale\\theta1.57_t0_10_20Z"
#distance_type = 'L2'
distance_type = 'KL'
symmetry_type = 'max'
write_index_matching = True;

txt_fpfh_files_source = []
txt_fpfh_files_target = []

files = [f for f in os.listdir(full_output_dir)]
for file in files:
    if '.txt' in file and '_source_' in file:
	    txt_fpfh_files_source.append(os.path.join(full_output_dir, file))
    elif '.txt' in file and '_target_' in file:
        txt_fpfh_files_target.append(os.path.join(full_output_dir, file))



eng = matlab.engine.start_matlab()
file = open(os.path.join(full_output_dir, "mean_dist.txt"), "w")
for f_source in txt_fpfh_files_source:
    for f_target in txt_fpfh_files_target:
        [mean_dist, nb_matching_points, nb_fpfh_source_points, nb_fpfh_target_points, nb_bins] = eng.getFPFHHistogramsDistance(f_source,f_target,write_index_matching,distance_type, nargout = 5)    
        # saving
        file.write("source : " + f_source + " target : " + f_target + "\n")
        file.write("nb points FPFH source, target : %i %i \n" % (nb_fpfh_source_points, nb_fpfh_target_points))
        file.write("nb points for matching : %i \n" % nb_matching_points )
        file.write("nb bins : %i \n" % nb_bins)
        file.write("mean_dist : " + "%5.6f\n" % mean_dist )		

file.close()