import subprocess
import os

# get all the pcd files in the subdirectory
current_path = os.path.dirname(os.path.realpath(__file__))

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(current_path):
    for file in f:
        if '.pcd' in file:
            files.append(os.path.join(r, file))


# compute FPFH features
executable = "C:/FPFH/generateFPFH_files/x64/Release/generateFPFH_files.exe"			
for f in files:
	args = executable + " " + f
	subprocess.call(args, stdin=None, stdout=None, stderr=None)