# Import the necessary packages
import argparse
import cv2

vidcap = cv2.VideoCapture('D:/AIG Video Processing/test.avi')
#vidcap = cv2.VideoCapture('C:/Users/Kevin/Dropbox/Project/AIG/Cleaned Tracking Codes/00003.MTS')
success,image = vidcap.read()
count = 0
while success:
  success,image = vidcap.read()
  success,image = vidcap.read()
  cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file
  if cv2.waitKey(10) == 27:                     # exit if Escape is hit
      break
  count += 1