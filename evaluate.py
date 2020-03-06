import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import numpy as np
import time

def detect(detector, convertToFloat, imgQuery, imgPathList):   

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # find the keypoints and descriptors
    kpQuery, desQuery = detector.detectAndCompute(imgQuery,None) 

    if (convertToFloat):
        desQuery = np.float32(desQuery)    
    
    for imgPath in imgPathList:

        img = cv2.imread(imgPath, 0)

        kpDB, desDB = detector.detectAndCompute(img,None)        

        if (convertToFloat):
            desDB = np.float32(desDB)

        matches = flann.knnMatch(desQuery,desDB,k=2)
        
        goodMatchesCount = 0

        for m,n in matches:
            if m.distance < 0.7*n.distance:
                goodMatchesCount = goodMatchesCount + 1

        print(str(imgPath) + ": " + str(goodMatchesCount) + " good matches.")

def main():
    imgQuery = cv2.imread('uploads/Testbilder/Frauenkirche/90.JPG', 0) # queryImage  

    imgPathList = []
    imgPathList.append('uploads/Testbilder/Frauenkirche/30.JPG')
    imgPathList.append('uploads/Testbilder/Frauenkirche/45.JPG')
    imgPathList.append('uploads/Testbilder/Frauenkirche/60.JPG')
    imgPathList.append('uploads/Testbilder/Frauenkirche/75.JPG')
    imgPathList.append('uploads/Testbilder/Frauenkirche/105.JPG')
    imgPathList.append('uploads/Testbilder/Frauenkirche/120.JPG')
    imgPathList.append('uploads/Testbilder/Frauenkirche/135.JPG')
    imgPathList.append('uploads/Testbilder/Frauenkirche/150.JPG')

    # Initiate detectors
    sift = cv2.xfeatures2d.SIFT_create()
    surf = cv2.xfeatures2d.SURF_create()
    brisk = cv2.BRISK_create()
    orb = cv2.ORB_create()
    kaze = cv2.KAZE_create()
    akaze = cv2.AKAZE_create()    

    startTime = time.time()
    goodMatches = detect(sift, False, imgQuery, imgPathList)
    endTime = time.time()
    print ("SIFT calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )

    startTime = time.time()
    goodMatches = detect(surf, False, imgQuery, imgPathList)
    endTime = time.time()
    print ("SURF calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )

    startTime = time.time()
    goodMatches = detect(brisk, True, imgQuery, imgPathList)
    endTime = time.time()
    print ("BRISK calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )

    startTime = time.time()
    goodMatches = detect(orb, True, imgQuery, imgPathList)
    endTime = time.time()
    print ("ORB calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )   

    startTime = time.time()
    goodMatches = detect(kaze, True, imgQuery, imgPathList)
    endTime = time.time()
    print ("KAZE calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )
    
    startTime = time.time()
    goodMatches = detect(akaze, True, imgQuery, imgPathList)
    endTime = time.time()
    print ("AKAZE calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )     

main()