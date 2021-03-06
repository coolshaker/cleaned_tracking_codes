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

	#Step 1. Use KLT tracker to capture the corner features and find their conrrespondence
	param_winsize=10 #search window size
	param_qlevel = 0.5 #qualityLevel
	isVisualize = False #visualization or not 
	#execfile("klt_func.py") #output "klt_XXX.mat" to output folder

	#Step 2. Delete low speed fatures 
	param_mspeed = 7 #minimum speed threshold
	execfile("trj_filter.py") #output .mat to filtered folder

	#Step 3. Find the connected components
	param_ovlpframes=15 #overlapped frame number
	param_dist = 200 #average distant differnce threshold
	param_yspeed = 3 #average yspeed difference threshold
	param_xspeed = 7 #average xspeed difference threshold
	execfile("trjcluster_func_SBS.py") #output .mat to adj folder

	#Step 4. Subspace clustering with Dirichlet process mixture model: first reduce the dimension of the data then do the clustering
	param_clusterindex=4 #greater value result in less clusters
	execfile("subspace_cluster.py") #output "00X.mat" to ssc folder 

	#Step 5. Compile trajectories in different trunks 
	execfile("unify_label_func.py") #output "Complete_result.mat" to ssc folder

	#Step 6. Convert from .mat to dictionary files
	isVisualize      = False
	execfile("trj2dic.py") #output pickle files to ssc folder 

	#Step 7. Pair vehicles 
	execfile('getVehiclesPairs.py') #output csv files to Output folder


