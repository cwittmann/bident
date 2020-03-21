import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import time

MIN_MATCH_COUNT = 10

startTime = time.time()

img1 = cv.imread('images/tyn1.png', 0) # queryImage
img2 = cv.imread('images/tyn2.png', 0) # trainImage

# Initiate AKAZE detector
akaze = cv.AKAZE_create()
# Find the keypoints and descriptors with SIFT
kp1, des1 = akaze.detectAndCompute(img1, None)
kp2, des2 = akaze.detectAndCompute(img2, None)

des1 = np.float32(des1)
des2 = np.float32(des2)

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1,des2,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)

img3 = cv.drawMatches(img1,kp1,img2,kp2,good,None, flags = 2)

endTime = time.time()
print (str(endTime - startTime) + " seconds" )

plt.imshow(img3, 'gray'),plt.show()