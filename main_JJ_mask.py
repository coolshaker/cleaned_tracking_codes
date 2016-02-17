import os
import cv2

for videoIndex in range(115,132):

	videoPath="D:/AIG Video Processing/Jay_Johnson_mask/"+"00"+str(videoIndex)+"_ROI.avi" #define the path of video or images
	outputPath="D:/AIG Video Processing/Jay_Johnson_mask/Output"+str(videoIndex)+"/"

	if not os.path.exists(outputPath):
	    os.makedirs(outputPath)
	if not os.path.exists(outputPath+"adj"):
	    os.makedirs(outputPath+"adj")
	if not os.path.exists(outputPath+"filtered"):
	    os.makedirs(outputPath+"filtered")
	if not os.path.exists(outputPath+"ssc"):
	    os.makedirs(outputPath+"ssc")

	isVideo = True
	fps = 5 #expected frame rate per sec (5 for fulton, and 6 for Johnson)
	fpsOrigin = cv2.VideoCapture(videoPath).get(5) #frame rate of the source
	subSampRate = int(round(fpsOrigin/fps)) #subsamprate
	trunclen = 600 #frames per trunk

	param_winsize=10 #
	param_qlevel = 0.5 #qualityLevel
	isVisualize = False #visualization or not 
	execfile("klt_func.py")

	param_mspeed = 3 #minimum speed
	execfile("trj_filter.py") #output to filtered folder

	param_dist = 250 #dth    = 100
	param_yspeed = 5 #yspdth = 2
	param_xspeed = 10 #xspdth = 4
	execfile("trjcluster_func_SBS.py") #output to adj folder

	param_clusterindex=4 #greater value result in less clusters
	execfile("subspace_cluster.py") #output "00X.mat" to ssc folder 

	execfile("unify_label_func.py") #output "Complete_result.mat" to ssc folder

	execfile("trj2dic.py") #output pickle files to ssc folder 

	execfile('getVehiclesPairs.py') #output csv files to Output folder

