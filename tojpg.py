# Import the necessary packages
import argparse
import cv2

vidcap = cv2.VideoCapture('D:/AIG Video Processing/Jay_Fulton/00016.MTS')
subSampRate=10

count = 0
#while success:
while count<20:
  #vidcap.set (cv2.CAP_PROP_POS_FRAMES,count*subSampRate)
  success,image = vidcap.read()
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1