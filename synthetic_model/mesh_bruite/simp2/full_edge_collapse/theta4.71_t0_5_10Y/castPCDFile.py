import matlab.engine
import os


# get all the pcd files in the subdirectory
current_path = os.path.dirname(os.path.realpath(__file__))

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(current_path):
    for file in f:
        if '.pcd' in file:
            files.append(os.path.join(r, file))


# cast to float the double coordinates of a pcd file
eng = matlab.engine.start_matlab()
for f in files:
	ptCloud = eng.pcread(f);
	pcFloatCoord = eng.single(ptCloud.Location);
	cast_ptCloud = eng.pointCloud(pcFloatCoord);
	eng.pcwrite(cast_ptCloud,f,'Encoding','ascii');
