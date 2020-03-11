from __future__ import print_function
import cv2 as cv
import numpy as np
import argparse
from math import sqrt
import matplotlib.pyplot as plt
import time

startTime = time.time()

img1 = cv.imread('images/tyn1.png', 0) # queryImage
img2 = cv.imread('images/tyn2.png', 0) # trainImage

# Initiate AKAZE detector
akaze = cv.AKAZE_create()
# Find the keypoints and descriptors with SIFT
kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)

# BFMatcher with default params
bf = cv.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)

# Apply ratio test
good_matches = []
for m,n in matches:
    if m.distance < 0.75*n.distance:
        good_matches.append([m])
        
# Draw matches
img3 = cv.drawMatchesKnn(img1,kp1,img2,kp2,good_matches,None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

endTime = time.time()
print (str(endTime - startTime) + " seconds" )

plt.imshow(img3, 'gray'),plt.show()