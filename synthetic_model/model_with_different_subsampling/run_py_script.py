import matlab.engine
import numpy as np
import subprocess
import os
import statistics
from shutil import copyfile
from pathlib import Path

# variables
source_filename = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\24_07_19\\input_meshes\\source\\ObjetSynthetique_simp32.ply'
target_filename = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\24_07_19\\input_meshes\\target\\ObjetSynthetique_simp64_edgeCollapse.ply'
output_directory = 'C:\\Registration\\Test\\meshRegistration\\synthetic_model\\24_07_19\\results'
initial_matching = 'False'
cross_check = 'False'

eng = matlab.engine.start_matlab()
eng.workspace['output_directory'] = output_directory
eng.workspace['source_filename'] = source_filename
eng.workspace['target_filename'] = target_filename
eng.eval("nb_pc_target = 1;", nargout = 0)
eng.eval("type_of_noise = 'gaussian';", nargout = 0)
eng.eval("noise_generation = 'auto';", nargout = 0)
eng.eval("noise_level_source  = 0.0", nargout = 0)
eng.eval("noise_level_target = 0.8;", nargout = 0)
eng.eval("nb_noise_matrix_source = 0;", nargout = 0)
eng.eval("nb_noise_matrix_target = 1;", nargout = 0)
eng.eval("cutting_plane = 'XZ';", nargout = 0)
eng.eval("ratio = 0.4;", nargout = 0)
eng.eval("theta = 3.14/2;", nargout = 0)
eng.eval("rot_axis = 'X';", nargout = 0)
eng.eval("trans = [0, 10, 6];", nargout = 0)
eng.eval("scale_coeff = [1, 1, 1];", nargout = 0)


# for loop to compute mean curves
for i in range(10):

     # generate input data (source and target files)
    [full_output_dir, source_name, target_name] = eng.eval("generate_inputs_for_FPFH_algorithm(output_directory, source_filename, target_filename, theta, rot_axis, trans, scale_coeff, cutting_plane, ratio, nb_pc_target, type_of_noise, noise_generation, nb_noise_matrix_source, noise_level_source, nb_noise_matrix_target, noise_level_target);", nargout = 3)

    # FGR registration
    downsampling_coeff_list = ['1.0', '0.9', '0.8', '0.7', '0.6', '0.5', '0.4', '0.3']
    for down_coeff  in downsampling_coeff_list:
        print(down_coeff)
        myProcess = subprocess.Popen(["python", "registration_workflow_v2.py", source_filename, full_output_dir, source_name, target_name, down_coeff, initial_matching, cross_check])
        myProcess.wait()
    
    
    
    # file header
    fgr_cc_result_file = os.path.join(full_output_dir, 'cc_results.txt')
    out_file =open(fgr_cc_result_file, "a+")
    out_file.write("test %d ending\n" % i+1)
    out_file.close()
    

    # ICP registration
    pcd_source_file = source_name + ".pcd"
    pcd_target_file = target_name + ".pcd"
    output_subdir = "ICP"

    #create ICP directory
    if not os.path.exists(os.path.join(full_output_dir, output_subdir)):
        os.mkdir(os.path.join(full_output_dir, output_subdir))
    copyfile(os.path.join(full_output_dir, pcd_target_file), os.path.join(full_output_dir, output_subdir, pcd_target_file))
    copyfile(os.path.join(full_output_dir, pcd_source_file), os.path.join(full_output_dir, output_subdir, pcd_source_file))


    # compute ICP registration
    cloudCompare_exe = "C:\\Program Files\\CloudCompare\\CloudCompare.exe"
    registered_pc_name = "registered_pc.pcd"
    args = cloudCompare_exe + " -SILENT" + " -o " + os.path.join(full_output_dir, output_subdir, pcd_target_file) + " -o " + os.path.join(full_output_dir, output_subdir, pcd_source_file) + " -NO_TIMESTAMP -AUTO_SAVE OFF -ICP -RANDOM_SAMPLING_LIMIT 3500 -C_EXPORT_FMT PCD -SAVE_CLOUDS FILE " + os.path.join(full_output_dir, output_subdir, registered_pc_name) + " FILE " + os.path.join(full_output_dir, output_subdir, pcd_source_file) # data file first and reference file second 
    subprocess.call(args, stdin=None, stdout=None, stderr=None)


    # compute point cloud to point cloud distance 
    # log_file = os.path.join(full_output_dir, output_subdir, 'log.txt')
    # open(log_file, 'a').close()
    icp_cc_result_file = os.path.join(full_output_dir, output_subdir, 'icp_cc_results.txt')
    open(icp_cc_result_file, 'a').close()
    args = cloudCompare_exe + " -SILENT" + " -o " + os.path.join(full_output_dir, output_subdir, registered_pc_name) + " -o " + os.path.join(full_output_dir, output_subdir, pcd_source_file) + " -NO_TIMESTAMP -C_EXPORT_FMT ASC -c2c_dist"  # compared file first and reference file second
    # args = cloudCompare_exe + " -o " + os.path.join(full_output_dir, output_subdir, registered_pc_name) + " -o " + source_filename + " -NO_TIMESTAMP -C_EXPORT_FMT ASC -c2m_dist -LOG_FILE " + log_file  # uncomment if you want to compute C2M distance
    subprocess.call(args, stdin=None, stdout=None, stderr=None)


   # process cloudCompare output
        # get file with c2c distance 
    path = Path(full_output_dir) / 'ICP'
    for file in os.listdir(path):
        if "C2C_DIST" in file and ".asc" in file:
            c2c_file = file

        # get everything in column 4
    col_num = 3
    col_data = []
    delimiter = " "
    with open(path / c2c_file) as f:
        data = f.readlines()
        for line in data:
            col_data.append(line.strip().split(delimiter)[col_num])

    mean_C2C_dist = statistics.mean(list(map(float, col_data)))
    print(mean_C2C_dist)
    std_C2C = statistics.stdev(list(map(float, col_data)))
    print(std_C2C)
    header = "objet source : " + source_name  + " ; objet target : " + target_name + "\n"
    out_file =open(icp_cc_result_file, "a+")
    out_file.write("%s" % header)
    out_file.write("Mean distance = %5.6f / std deviation = %5.6f\n" % (mean_C2C_dist,std_C2C))
    out_file.close()


    # f=open(log_file, "r")
    # fl = f.readlines()
    # for line in fl:
        # if "[ComputeDistances]" in line: 
            # out_file =open(icp_cc_result_file, "a+")
            # out_file.write("%s" % line)
            # out_file.close()
    # f.close()



# matlab plot
fgr_cc_result_file = os.path.join(full_output_dir, 'cc_results.txt')
figure = eng.draw_pointCloud_to_pointCloud_meanDistance(fgr_cc_result_file, icp_cc_result_file)


 