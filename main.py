import os
import cv2

videoPath="D:/AIG Video Processing/AVI_mask/test_mask.avi"#define the path of video or images
outputPath="D:/AIG Video Processing/AVI_mask/Output/"

if not os.path.exists(outputPath):
    os.makedirs(outputPath)
if not os.path.exists(outputPath+"adj"):
    os.makedirs(outputPath+"adj")
if not os.path.exists(outputPath+"filtered"):
    os.makedirs(outputPath+"filtered")
if not os.path.exists(outputPath+"ssc"):
    os.makedirs(outputPath+"ssc")


isVideo  = True
fps=5 #expected frame rate per sec (5 for fulton, and 6 for Johnson)
fpsOrigin= cv2.VideoCapture(videoPath).get(5) #frame rate of the source
subSampRate = int(round(fpsOrigin/fps)) #subsamprate
trunclen=600 #frames per trunk

#execfile("klt_func.py")
execfile("trj_filter.py") #output to filtered folder
execfile("trjcluster_func_SBS.py") #output to adj folder
execfile("subspace_cluster.py") #output to ssc folder
execfile("unify_label_func.py") #output to ssc folder
execfile("trj2dic.py") #output to ssc folder
execfile('getVehiclesPairs.py') #output to Output folder

