import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

imgQuery = cv2.imread('uploads/Testbilder/Nacht/SchuerstabhausT.JPG', 0) # queryImage  

imgPathList = []
imgPathList.append('uploads/Testbilder/Nacht/SchuerstabhausN.JPG')


# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)

# find the keypoints and descriptors with SIFT
kpQuery, desQuery = sift.detectAndCompute(imgQuery,None)    

for imgPath in imgPathList:

    img = cv2.imread(imgPath, 0)

    kpDB, desDB = sift.detectAndCompute(img,None)        
    matches = flann.knnMatch(desQuery,desDB,k=2)
        
    goodMatchesCount = 0

    for m,n in matches:
        if m.distance < 0.7*n.distance:
            goodMatchesCount = goodMatchesCount + 1

    print(imgPath)
    print("Good matches found: " + str(goodMatchesCount))            

  


