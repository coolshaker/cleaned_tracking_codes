import cv2
import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import cPickle as pickle

videoPath="D:/AIG Video Processing/AVI_mask/test_mask.avi"
outputPath="D:/AIG Video Processing/AVI_mask/Output/"
subSampRate=2

vctime  = pickle.load( open( outputPath+"ssc/final_vctime.p", "rb" ) )
vcxtrj  = pickle.load( open( outputPath+"ssc/final_vcxtrj.p", "rb" ) )
vcytrj  = pickle.load( open( outputPath+"ssc/final_vcytrj.p", "rb" ) )


# - get the total frame number
frameNum=0
for vehID in vctime.keys():
	try:
		if vctime[vehID][1]>frameNum:
			frameNum=vctime[vehID][1]
	except:
		pass

# - find the vehs in each frame
labinT={}
for frame_idx in range(1,frameNum+1):
	labTemp=[]
	for vehID in vctime.keys():
		try:
			if frame_idx>=vctime[vehID][0] and frame_idx<=vctime[vehID][1]:
				labTemp.append(vehID)
		except:
			pass
	
	labinT[frame_idx]=labTemp


# - visualization
startFrame=500
endFrame=6000
cap         = cv2.VideoCapture(videoPath)
st,firstfrm = cap.read()
 
nrows     = int(np.size(firstfrm,0))
ncols     = int(np.size(firstfrm,1))
fig = plt.figure('vis')
axL = plt.subplot(1,1,1)
im  = plt.imshow(np.zeros([nrows,ncols,3]))
plt.axis('off')
plt.ion()

cap.set (cv2.CAP_PROP_POS_FRAMES,0)
for frame_idx in range(startFrame,endFrame):
	
	cap.set (cv2.CAP_PROP_POS_FRAMES,frame_idx*subSampRate)
	 
	status, frame = cap.read()

	im.set_data(frame[:,:,::-1])
	print labinT[frame_idx]
	for vehID in labinT[frame_idx]:
	#for vehID in [225]:
		currIndex=frame_idx-vctime[vehID][0]-1
		preIndex=frame_idx-vctime[vehID][0]-2
		if preIndex>0 and currIndex<len(vcxtrj[vehID]):
			lines       = axL.plot([vcxtrj[vehID][preIndex],vcxtrj[vehID][currIndex]],[vcytrj[vehID][preIndex],vcytrj[vehID][currIndex]],color = 'r',linewidth=1)
		
	plt.draw() #or fig.canvas.draw()
	plt.pause(0.001) #or plt.show()
	#axL.lines.pop(0) #remove the previous trajectories
	#plt.show()


